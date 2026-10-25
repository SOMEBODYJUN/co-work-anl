"""Full finite-type separation for the true-H 6565-row payment system."""
import price_indexed_hinges as p
import trueH_payment_pricing as th
if __name__=='__main__':p.run(4,th.Universe,'trueH_payment_discovery.json','trueH_payment_fullpricing.json')
