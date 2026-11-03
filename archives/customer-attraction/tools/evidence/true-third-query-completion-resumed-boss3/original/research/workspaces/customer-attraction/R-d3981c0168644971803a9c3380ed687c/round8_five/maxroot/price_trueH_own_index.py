"""Continue all-type pricing until a >2 primal or a globally unviolated dual.

The source's T/U/V/W repeated-query class is completed. Prior frozen search
files remain separate. No floating result is promoted to an exact theorem.
"""
import price_indexed_hinges as p
import trueH_own_index_pricing as own
if __name__=='__main__':p.run(100,own.Universe,'trueH_own_index_discovery.json','trueH_own_index_fullpricing.json',max_new_columns=400,per_state_batch=16,target_beta=2)
