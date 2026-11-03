"""Full type target-two pricing with all eight actual HQR states retained."""
import price_indexed_hinges as p
import actual13_payment_pricing as a
if __name__=='__main__':p.run(100,a.Universe,'actual13_payment_discovery.json','actual13_payment_fullpricing.json',max_new_columns=400,per_state_batch=16,target_beta=2)
