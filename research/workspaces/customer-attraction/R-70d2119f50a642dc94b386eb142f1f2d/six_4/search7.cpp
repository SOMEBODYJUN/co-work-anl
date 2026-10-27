// Exploratory exact six-player SPE search for seven maximal catalog topics.
// Every payoff is stored in sixtieths; arbitrary history-dependent tie choices
// are represented by the entire set of achievable continuation terminal counts.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

using namespace std;
constexpr int M=6, P=7, NT=127, BASE=7;
using Key=array<uint8_t,P>;
struct State { Key q{}; int sum=0; array<int,P> child{}; int terminal=-1; };
vector<State> st;
vector<int> layers[M+1];
int id[823543];
array<Key,924> terms;
int termnum=0;

int encode(Key const &q) { int z=0; for(int x:q) z=z*BASE+x; return z; }
void enumq(Key &q,int a,int left,int total) {
    if(a==P-1) {
        if(left>6) return;
        q[a]=left; State s; s.q=q; s.sum=total;
        int k=encode(q); id[k]=st.size();
        if(total==M) { s.terminal=termnum; terms[termnum++]=q; }
        layers[total].push_back(st.size()); st.push_back(s); return;
    }
    for(int v=0;v<=left;v++) { q[a]=v; enumq(q,a+1,left-v,total); }
}
void initialize() {
    fill(begin(id),end(id),-1);
    Key q{};
    for(int n=0;n<=M;n++) enumq(q,0,n,n);
    if(termnum!=924) { cerr<<"term count "<<termnum<<"\n"; abort(); }
    for(auto &s:st) if(s.sum<M) for(int a=0;a<P;a++) {
        Key qq=s.q; ++qq[a]; s.child[a]=id[encode(qq)];
        if(s.child[a]<0) abort();
    }
}
struct Game {
    array<int,NT+1> w{};
    int utility[924][P]{};
    int welfare[924]{};
    vector<vector<int>> R;
    array<int,924> stamp{};
    int serial=0;
    int rootTerm=-1, rootW=0, opt=0;
    Game():R(st.size()){}
    void solve() {
        int total=0, minPrivate=numeric_limits<int>::max();
        for(int a=0;a<P;a++) minPrivate=min(minPrivate,w[1<<a]);
        for(int mask=1;mask<=NT;mask++) total+=w[mask];
        opt=total-minPrivate;
        for(int t=0;t<termnum;t++) {
            auto const &q=terms[t];
            welfare[t]=0;
            fill(begin(utility[t]),end(utility[t]),0);
            for(int mask=1;mask<=NT;mask++) if(w[mask]) {
                int den=0;
                for(int a=0;a<P;a++) if(mask&(1<<a)) den+=q[a];
                if(!den) continue;
                welfare[t]+=w[mask];
                int amount=w[mask]*60/den;
                for(int a=0;a<P;a++) if(mask&(1<<a)) utility[t][a]+=amount;
            }
        }
        for(int j:layers[M]) { auto &v=R[j]; v.clear(); v.push_back(st[j].terminal); }
        for(int depth=M-1;depth>=0;depth--) for(int j:layers[depth]) {
            State const &s=st[j]; int val[P], threshold=numeric_limits<int>::min();
            for(int a=0;a<P;a++) {
                val[a]=numeric_limits<int>::max();
                auto const &child=R[s.child[a]];
                for(int t:child) val[a]=min(val[a],utility[t][a]);
                if(child.empty()) abort();
                threshold=max(threshold,val[a]);
            }
            auto &v=R[j]; v.clear(); ++serial;
            for(int a=0;a<P;a++) for(int t:R[s.child[a]])
                if(utility[t][a]>=threshold && stamp[t]!=serial) {
                    stamp[t]=serial; v.push_back(t);
                }
            if(v.empty()) abort();
        }
        int root=id[0]; rootTerm=-1; rootW=numeric_limits<int>::max();
        for(int t:R[root]) if(welfare[t]<rootW) {rootW=welfare[t];rootTerm=t;}
    }
};

void print(Game const &g,int eval) {
    cout<<"eval "<<eval<<" ratio "<<double(g.rootW)/g.opt
        <<" W "<<g.rootW<<" OPT "<<g.opt<<" margin "<<2*g.rootW-g.opt
        <<" terminal";
    for(auto c:terms[g.rootTerm]) cout<<" "<<int(c);
    cout<<"\nweights";
    for(int k=1;k<=NT;k++) if(g.w[k]) cout<<" "<<k<<":"<<g.w[k];
    cout<<"\n"<<flush;
}
int main(int argc,char **argv) {
    initialize();
    int runs=argc>1?atoi(argv[1]):10000;
    uint64_t seed=argc>2?strtoull(argv[2],nullptr,10):192711;
    mt19937_64 rng(seed);
    Game g, best;
    double bestRatio=1e9;
    int evaluation=0;
    for(int restart=0;evaluation<runs;restart++) {
        g.w.fill(0);
        for(int a=0;a<P;a++) g.w[1<<a]=1+rng()%6;
        int support=8+rng()%28;
        for(int k=0;k<support;k++) {
            int mask=1+rng()%NT;
            if(__builtin_popcount(unsigned(mask))==1) continue;
            g.w[mask]+=1+rng()%25;
        }
        int nlocal=50+rng()%150;
        for(int loop=0;loop<nlocal && evaluation<runs;loop++) {
            g.solve(); evaluation++;
            double ratio=double(g.rootW)/g.opt;
            if(ratio<bestRatio-1e-12) { bestRatio=ratio; best.w=g.w; print(g,evaluation); }
            if(2*g.rootW<g.opt) return 0;
            int mask=1+rng()%NT;
            int old=g.w[mask];
            int delta=int(rng()%21)-10;
            if(!delta) delta=1;
            g.w[mask]=max(__builtin_popcount(unsigned(mask))==1?1:0,old+delta);
            g.solve(); evaluation++;
            double newRatio=double(g.rootW)/g.opt;
            double temp=0.05*(1.0-double(loop)/nlocal)+0.005;
            if(newRatio<bestRatio-1e-12) { bestRatio=newRatio; best.w=g.w; print(g,evaluation); }
            if(2*g.rootW<g.opt) return 0;
            if(newRatio>ratio && uniform_real_distribution<double>(0.0,1.0)(rng)>exp((ratio-newRatio)/temp)) g.w[mask]=old;
        }
    }
    cerr<<"search complete seed "<<seed<<" evaluations "<<evaluation<<" best ratio "<<bestRatio<<"\n";
}
