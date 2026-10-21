#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
const int T=7,M=5,L=60,K=(1<<T);
struct State {array<int,T> q;array<int,T> child;int n;vector<int> out;};
vector<State> st;map<array<int,T>,int> ix;vector<array<int,T>> ts;vector<array<int,K>> den;vector<array<int,T>> util;vector<int> welfare;
void gen(int a,int left,array<int,T>&q,int n){if(a==T-1){q[a]=left;State s;s.q=q;s.n=n;ix[q]=st.size();st.push_back(s);return;}for(int z=0;z<=left;z++){q[a]=z;gen(a+1,left-z,q,n);}}
void init(){array<int,T>q{};for(int n=0;n<=M;n++)gen(0,n,q,n);for(auto&s:st){if(s.n<M){for(int a=0;a<T;a++){auto z=s.q;z[a]++;s.child[a]=ix[z];}}else{s.out={int(ts.size())};ts.push_back(s.q);}}for(auto&q:ts){array<int,K>d{};for(int mask=1;mask<K;mask++){int bit=__builtin_ctz(mask);d[mask]=d[mask^(1<<bit)]+q[bit];}den.push_back(d);}util.resize(ts.size());welfare.resize(ts.size());}
struct Result{int opt,worst,ti;bool operator<(const Result&b)const{return 1LL*opt*b.worst<1LL*b.opt*worst;}};
Result eval(const array<int,K>&w){int opt=0;for(int t=0;t<(int)ts.size();t++){util[t].fill(0);welfare[t]=0;for(int mask=1;mask<K;mask++)if(w[mask]&&den[t][mask]){welfare[t]+=w[mask];int val=w[mask]*(L/den[t][mask]);for(int a=0;a<T;a++)if((mask&(1<<a))&&ts[t][a])util[t][a]+=val;}opt=max(opt,welfare[t]);}
 vector<int> mark(ts.size(),-1);for(int si=(int)st.size()-1;si>=0;si--){auto&s=st[si];if(s.n==M)continue;int floor=0;for(int a=0;a<T;a++){int mn=2147483647;for(int t:st[s.child[a]].out)mn=min(mn,util[t][a]);floor=max(floor,mn);}s.out.clear();for(int a=0;a<T;a++)for(int t:st[s.child[a]].out)if(util[t][a]>=floor&&mark[t]!=si){mark[t]=si;s.out.push_back(t);}}
 int worst=2147483647,ti=-1;for(int t:st[0].out)if(welfare[t]<worst){worst=welfare[t];ti=t;}return{opt,worst,ti};}
void save(const string&path,const array<int,K>&w,Result r,int it){ofstream f(path);f<<"{\"players\":"<<M<<",\"topics\":[\"A\",\"B\",\"C\",\"D\",\"E\",\"F\",\"G\"],\"customers\":[";bool first=true;for(int mask=1;mask<K;mask++)if(w[mask]){if(!first)f<<",";first=false;f<<"{\"topics\":[";bool ff=true;for(int a=0;a<T;a++)if(mask&(1<<a)){if(!ff)f<<",";ff=false;f<<a;}f<<"],\"multiplicity\":"<<w[mask]<<"}";}f<<"],\"search\":{\"opt\":"<<r.opt<<",\"minimum\":"<<r.worst<<",\"iteration\":"<<it<<",\"terminal\":[";for(int a=0;a<T;a++){if(a)f<<",";f<<ts[r.ti][a];}f<<"]}}\n";}
int main(int argc,char**argv){init();int rounds=argc>1?stoi(argv[1]):200000;int seed=argc>2?stoi(argv[2]):1;string path=argc>3?argv[3]:"best.json";mt19937 rng(seed);array<int,K>bestw{},w{};Result best{0,1,0},cur;int stay=0;for(int it=0;it<rounds;it++){if(it%3000==0||stay>1000){w.fill(0);if((it/3000)%3!=2){int big=rng()%T;w[1<<big]=M;int count=0;for(int a=0;a<T&&count<M-1;a++)if(a!=big){w[1<<a]=1;count++;}if((it/3000)%3==1)for(int j=0;j<5;j++)w[1+rng()%(K-1)]+=rng()%3;}else{for(int j=0;j<12;j++)w[1+rng()%(K-1)]+=1+rng()%15;}cur=eval(w);stay=0;}auto v=w;int changes=(rng()%10==0)?2+rng()%8:1;for(int j=0;j<changes;j++){int mask=1+rng()%(K-1);if(rng()%4==0){vector<int>nz;for(int b=1;b<K;b++)if(v[b])nz.push_back(b);if(!nz.empty())mask=nz[rng()%nz.size()];}int delta=(rng()%5==0)?1+rng()%10:1;if(rng()%2)delta=-delta;v[mask]=max(0,min(200,v[mask]+delta));}auto r=eval(v);if(cur<r ||(1LL*cur.opt*r.worst==1LL*r.opt*cur.worst&&rng()%4==0)){w=v;cur=r;stay=0;}else stay++;if(best<cur){best=cur;bestw=w;save(path,w,best,it);cout<<"seed "<<seed<<" iteration "<<it<<" ratio "<<best.opt<<"/"<<best.worst<<"="<<(double)best.opt/best.worst<<" types "<<count_if(w.begin(),w.end(),[](int z){return z>0;})<<endl;}if(it%10000==0)cerr<<it<<" "<<(double)best.opt/best.worst<<"\n";}}
