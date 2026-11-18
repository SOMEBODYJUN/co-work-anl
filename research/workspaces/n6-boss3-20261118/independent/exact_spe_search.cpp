// Exact full-history pure-SPE outcome recursion for six players and a common finite catalogue.
// Integer atom weights represent that many distinct unit-value clients of each membership mask.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <string>
#include <vector>
using namespace std;
struct State { vector<int> c; int depth; vector<int> child; vector<int> eligible; };
struct Solver {
 int A; vector<State> st; vector<vector<int>> layer; map<vector<int>,int> ids; vector<int> finals, weights; vector<array<long long,8>> payoff; vector<long long> welfare; long long total=0; int rootWorst=-1; long long bestW=0;
 Solver(int a):A(a),layer(7),weights(1<<a) {vector<int> c(A); for(int d=0;d<=6;d++)gen(c,0,d,d); for(auto& s:st){s.child.resize(A,-1); if(s.depth<6)for(int a=0;a<A;a++){auto z=s.c;z[a]++;s.child[a]=ids.at(z);}} finals=layer[6]; payoff.resize(finals.size());welfare.resize(finals.size());}
 void gen(vector<int>& c,int at,int remain,int d){if(at==A-1){c[at]=remain;int id=st.size();ids[c]=id;st.push_back({c,d,{},{}});layer[d].push_back(id);return;}for(int v=0;v<=remain;v++){c[at]=v;gen(c,at+1,remain-v,d);}}
 pair<long long,long long> run(const vector<int>& w){weights=w;total=accumulate(w.begin(),w.end(),0LL);for(int j=0;j<(int)finals.size();j++){payoff[j].fill(0);welfare[j]=0;auto& c=st[finals[j]].c;for(int mask=1;mask<(1<<A);mask++)if(w[mask]){int load=0;for(int a=0;a<A;a++)if(mask>>a&1)load+=c[a];if(load){welfare[j]+=w[mask];for(int a=0;a<A;a++)if(mask>>a&1)payoff[j][a]+=60LL*w[mask]/load;}}st[finals[j]].eligible.assign(1,j);}
 for(int d=5;d>=0;d--)for(int id:layer[d]){auto&s=st[id];long long threshold=0;for(int a=0;a<A;a++){long long mn=INT64_MAX;for(int j:st[s.child[a]].eligible)mn=min(mn,payoff[j][a]);threshold=max(threshold,mn);}s.eligible.clear();for(int a=0;a<A;a++)for(int j:st[s.child[a]].eligible)if(payoff[j][a]>=threshold)s.eligible.push_back(j);sort(s.eligible.begin(),s.eligible.end());s.eligible.erase(unique(s.eligible.begin(),s.eligible.end()),s.eligible.end());}
 bestW=INT64_MAX;rootWorst=-1;for(int j:st[0].eligible)if(welfare[j]<bestW){bestW=welfare[j];rootWorst=j;}return {bestW,total}; }
 void dump(ostream& out){out<<"actions "<<A<<" players 6\nweights";for(int v:weights)out<<' '<<v;out<<"\nW "<<bestW<<" OPT "<<total<<" root_outcomes "<<st[0].eligible.size()<<"\nfinal_counts";for(int v:st[finals[rootWorst]].c)out<<' '<<v;out<<"\npayoff_times_60";for(int a=0;a<A;a++)out<<' '<<payoff[rootWorst][a];out<<'\n';}
};
int main(int argc,char**argv){int A=argc>1?stoi(argv[1]):6;int rounds=argc>2?stoi(argv[2]):10000;unsigned seed=argc>3?stoul(argv[3]):712046;Solver s(A);mt19937 rng(seed);vector<int>w(1<<A),bestw;double best=1;auto start=chrono::steady_clock::now();for(int r=0;r<rounds;r++){
 if(r%1000==0||bestw.empty()) {fill(w.begin(),w.end(),0);int atoms=2+rng()%(2*A+1);for(int k=0;k<atoms;k++){int mask=1+rng()%((1<<A)-1);w[mask]+=1+rng()%30;}}
 else {w=bestw;int changes=1+rng()%4;for(int k=0;k<changes;k++){int mask=1+rng()%((1<<A)-1);if(rng()%4==0)w[mask]=0;else w[mask]=max(0,min(200,w[mask]+int(rng()%15)-7));}}
 auto [W,T]=s.run(w);if(!T)continue;double ratio=double(W)/T;if(ratio<best){best=ratio;bestw=w;cerr<<"round "<<r<<" ratio "<<W<<'/'<<T<<" = "<<ratio<<"\n";s.dump(cout);cout.flush();} }
 cerr<<"elapsed "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"s\n";
}
