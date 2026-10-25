"""Full type pricing for the known true-H 15-fixed-query completion."""
import price_indexed_hinges as p
import trueH_fixed_closure_pricing as fc
if __name__=='__main__':p.run(4,fc.Universe,'trueH_fixed_closure_discovery.json','trueH_fixed_closure_fullpricing.json')
