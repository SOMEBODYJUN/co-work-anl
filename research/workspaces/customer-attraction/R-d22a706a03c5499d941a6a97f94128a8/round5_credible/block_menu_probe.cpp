#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

// Exact set-valued backwards induction for n disjoint 16-customer modules.
// Utility values are integers in units 1/lcm(1,...,4*n). No floating point.
// Count memoization retains every admissible continuation outcome, so it does
// not impose a common selector on equal-count ordered histories.
struct Node {std::vector<uint64_t> outcomes; int floor=0;};
int blocks, players, topics, scale;
std::unordered_map<uint64_t,Node> memo;
std::array<std::array<int,4>,65536> utility;
uint64_t states=0, terminals=0, retained=0, comparisons=0;
int gcd(int a,int b){while(b){int c=a%b;a=b;b=c;}return a;}
int payoff(uint64_t q,int a){return utility[(q>>(16*(a/4)))&65535][a%4];}
int depth(uint64_t q){int t=0;for(int a=0;a<topics;++a)t+=(q>>(4*a))&15;return t;}
const Node& solve(uint64_t q,int d){
 auto seen=memo.find(q);if(seen!=memo.end())return seen->second;
 Node node;
 if(d==players){node.outcomes={q};++terminals;}
 else {
  std::vector<const Node*> children;
  for(int a=0;a<topics;++a)children.push_back(&solve(q+(uint64_t(1)<<(4*a)),d+1));
  for(int a=0;a<topics;++a){int low=1000000000;for(uint64_t t:children[a]->outcomes)low=std::min(low,payoff(t,a));node.floor=std::max(node.floor,low);}
  for(int a=0;a<topics;++a)for(uint64_t t:children[a]->outcomes){++comparisons;if(payoff(t,a)>=node.floor)node.outcomes.push_back(t);}
  std::sort(node.outcomes.begin(),node.outcomes.end());node.outcomes.erase(std::unique(node.outcomes.begin(),node.outcomes.end()),node.outcomes.end());
 }
 ++states;retained+=node.outcomes.size();
 auto it=memo.emplace(q,std::move(node)).first;
 if(states%500000==0)std::cerr<<"states "<<states<<" retained "<<retained<<"\n";
 return it->second;
}
uint64_t encode(std::array<int,4> local,int b){uint64_t q=0;for(int a=0;a<4;++a)q|=uint64_t(local[a])<<(16*b+4*a);return q;}
std::string fraction(int a){int g=gcd(a,scale);return std::to_string(a/g)+"/"+std::to_string(scale/g);}
void print_counts(std::ostream& out,uint64_t q){out<<"[";for(int a=0;a<topics;++a){if(a)out<<",";out<<((q>>(4*a))&15);}out<<"]";}
int main(int argc,char**argv){
 blocks=argc>1?std::stoi(argv[1]):3;if(blocks<1||blocks>3){std::cerr<<"This version uses 4-bit counts and is limited to n<=3.\n";return 2;}players=topics=4*blocks;scale=1;for(int j=2;j<=players;++j)scale=scale/gcd(scale,j)*j;
 for(int code=0;code<65536;++code){int a=code&15,b=(code>>4)&15,c=(code>>8)&15,d=(code>>12)&15;if(a+b+c+d>players)continue;auto div=[&](int n,int den){return den?n*(scale/den):0;};int common=div(1,a+b+c+d);utility[code]={div(2,a)+div(6,a+c)+common,div(4,b+d)+common,div(6,a+c)+div(3,c+d)+common,div(4,b+d)+div(3,c+d)+common};}
 memo.max_load_factor(0.8);memo.reserve(blocks==3?2800000:15000);auto start=std::chrono::steady_clock::now();const Node& root=solve(0,0);
 std::array<std::array<int,4>,4> cols={{{2,0,1,1},{1,1,1,1},{1,0,2,1},{1,0,1,2}}};std::array<int,4> base={2,1,1,0};uint64_t target_base=0;for(int b=1;b<blocks;++b)target_base|=encode(base,b);
 std::cout<<"{\"schema\":\"B10_BLOCK_MENU_SET_BI_PROBE_V1\",\"blocks\":"<<blocks<<",\"players\":"<<players<<",\"scale\":"<<scale<<",\"count_states\":"<<states<<",\"terminal_states\":"<<terminals<<",\"retained_outcomes\":"<<retained<<",\"root_floor\":\""<<fraction(root.floor)<<"\",\"root_outcome_count\":"<<root.outcomes.size()<<",\"columns\":[";
 for(int a=0;a<4;++a){uint64_t prefix=uint64_t(1)<<(4*a),target=target_base|encode(cols[a],0);const Node& child=solve(prefix,1);if(a)std::cout<<",";std::cout<<"{\"action\":"<<a<<",\"prefix_floor\":\""<<fraction(child.floor)<<"\",\"target\":";print_counts(std::cout,target);std::cout<<",\"feasible\":"<<(std::binary_search(child.outcomes.begin(),child.outcomes.end(),target)?"true":"false")<<",\"root_actor_payoff\":\""<<fraction(payoff(target,a))<<"\"";
  int minimum=1000000000,number=0,blocked=0;uint64_t witness=0;std::map<int,int> distribution;
  std::function<void(int,uint64_t,int)> boundary=[&](int j,uint64_t p,int remaining_low){
   if(j==topics){if(remaining_low!=1)return;++number;int f=solve(p,depth(p)).floor;++distribution[f];if(f>13*scale/4)++blocked;if(f<minimum){minimum=f;witness=p;}return;}
   int t=(target>>(4*j))&15;bool low=payoff(target,j)<=13*scale/4;
   for(int count=0;count<=t;++count){int rem=remaining_low+(low?t-count:0);if(rem<=1)boundary(j+1,p|(uint64_t(count)<<(4*j)),rem);}
  };boundary(0,0,0);
  std::cout<<",\"last_low_boundary\":{\"nodes\":"<<number<<",\"strictly_blocked\":"<<blocked<<",\"minimum_floor\":\""<<fraction(minimum)<<"\",\"witness\":";print_counts(std::cout,witness);std::cout<<",\"floor_distribution\":{";bool comma=false;for(auto e:distribution){if(comma)std::cout<<",";comma=true;std::cout<<"\""<<fraction(e.first)<<"\":"<<e.second;}std::cout<<"},\"witness_action_floors\":[";
  for(int j=0;j<topics;++j){int low=1000000000;uint64_t arg=0;const Node& cj=solve(witness+(uint64_t(1)<<(4*j)),depth(witness)+1);for(uint64_t t:cj.outcomes)if(payoff(t,j)<low){low=payoff(t,j);arg=t;}if(j)std::cout<<",";std::cout<<"{\"action\":"<<j<<",\"minimum\":\""<<fraction(low)<<"\",\"worst_outcome\":";print_counts(std::cout,arg);std::cout<<"}";}std::cout<<"]}";
  int extra_scale=scale/gcd(scale,players+1)*(players+1),best=-1,count=0;uint64_t best_target=0;
  for(uint64_t terminal:child.outcomes){if(payoff(terminal,a)>13*scale/4)continue;++count;int value=0;for(int b=0;b<blocks;++b){int code=(terminal>>(16*b))&65535;int aa=code&15,bb=(code>>4)&15,cc=(code>>8)&15,dd=(code>>12)&15;value+=4*(extra_scale/(1+bb+dd))+3*(extra_scale/(1+cc+dd))+extra_scale/(1+aa+bb+cc+dd);}if(value>best){best=value;best_target=terminal;}}
  int den=extra_scale*blocks,g=gcd(best,den);std::cout<<",\"uniform_D_query\":{\"admissible_outcomes\":"<<count<<",\"best_value\":\""<<best/g<<"/"<<den/g<<"\",\"target\":";print_counts(std::cout,best_target);std::cout<<",\"actor_payoff\":\""<<fraction(payoff(best_target,a))<<"\",\"strictly_above_u\":"<<(4*best>13*den?"true":"false")<<"}}";
 }
 std::array<std::array<int,4>,6> local_root={{{1,0,1,2},{1,0,2,1},{1,1,2,0},{2,0,0,2},{2,0,1,1},{2,1,1,0}}};int outside_local=0,multi_base=0;for(uint64_t t:root.outcomes){int bases=0;for(int b=0;b<blocks;++b){uint64_t local=(t>>(16*b))&65535;bool found=false;for(auto q:local_root)if(local==encode(q,0))found=true;if(!found)++outside_local;if(local==encode(base,0))++bases;}if(bases>=2)++multi_base;}
 uint64_t formula=1;for(int b=0;b<blocks;++b)formula*=5;uint64_t expected=formula+blocks*(formula/5);
 auto elapsed=std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now()-start).count();std::cout<<"],\"finite_root_profile_diagnostic\":{\"root_outcomes_outside_six_local_profiles\":"<<outside_local<<",\"root_outcomes_with_two_q0_blocks\":"<<multi_base<<",\"six_profiles_with_at_most_one_q0_count\":"<<expected<<",\"root_outcome_count_matches\":"<<(root.outcomes.size()==expected?"true":"false")<<"},\"elapsed_ms\":"<<elapsed<<"}\n";
}
