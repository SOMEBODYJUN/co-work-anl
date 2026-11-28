"use strict";
const fs=require("fs"),path=require("path"),E=require("./engine.js");
function save(name,value){fs.writeFileSync(path.join(__dirname,name),JSON.stringify(value,null,2)+"\n");}
const knownTerms={
  loans:{allowFull:true,prepayMax:"unlimited",prepayPeriodMax:"unlimited",salePayoffRule:"same_terms",salePayoffFeeBase:"balance",canPrepay:true,prepayFrom:1,prepayMin:0,prepayFee:0,settlementFee:0,transferWithLien:false,allowRecast:true,allowShorten:true},
  properties:{canSell:true,lock:1,saleLag:0,saleFee:0,closingFee:0},
  vehicles:{canSell:true,lock:1,saleLag:0,saleFee:0,closingFee:0,necessary:false},
  financial:{fee:0,settle:0,unlock:1,maturity:0,restriction:"free",purpose:"家庭可用"}
};
function row(group,fields){return {...E.templates[group],...knownTerms[group],...fields};}
function scenario(id,name,role,entries){
  const source="design-"+id;
  return {id,name,role,description:"人为压力测试。参数可编辑，数值用于比较指定路径下的家庭履约和现金，不表示中国经济预测或事件概率。",
    paths:entries.map(([key,value,start=1,duration=120,target="*"])=>E.path(key,value,start,duration,target,source))};
}
const paths=[
  scenario("continuity","结构延续","continuity",[
    ["propertyShock",-.06],["propertyAnnual",-.015,1,36],["rentFactor",.95,1,36],["vacancyAdd",.04,1,36],
    ["wageFactor",.98,1,24],["businessFactor",.94,1,24],["unemploymentMonths",0],["recoveryMonths",3],["reemploymentFactor",1],
    ["financialShock",-.08],["securityAnnual",.01],["concentrationHaircut",.04],["inflationAnnual",.015],
    ["cashRateDelta",0],["loanRateDelta",0],["saleHaircut",.03,1,36],["saleDelay",2,1,36]
  ]),
  scenario("severe","严重下行与信用损失","severe",[
    ["propertyShock",-.25],["propertyAnnual",-.025,1,36],["rentFactor",.78,1,48],["vacancyAdd",.12,1,48],
    ["wageFactor",.82,1,36],["businessFactor",.65,1,36],["unemploymentMonths",8,4,1],["recoveryMonths",8],["reemploymentFactor",.88],
    ["financialShock",-.35],["securityAnnual",-.025,1,36],["concentrationHaircut",.12],["inflationAnnual",.025],
    ["cashRateDelta",-.005],["loanRateDelta",.015,1,48],["saleHaircut",.12,1,48],["saleDelay",7,1,48]
  ]),
  scenario("recovery","有效恢复","recovery",[
    ["propertyAnnual",.02,1,60],["rentFactor",1.04,1,48],["vacancyAdd",-.02,1,48],["wageFactor",1.06,1,60],
    ["businessFactor",1.12,1,60],["unemploymentMonths",0],["recoveryMonths",2],["reemploymentFactor",1],
    ["securityAnnual",.035,1,60],["concentrationHaircut",0],["inflationAnnual",.02],["cashRateDelta",0],
    ["loanRateDelta",-.005,1,60],["saleHaircut",0],["saleDelay",0]
  ])
];
const h={...E.blank(),dataKind:"synthetic_example",cash:280000,cashAnnual:.012,reserveMonths:3,minimumLiving:6000,cutFraction:.55,maxSaleWait:24,
  incomes:[
    row("incomes",{id:"pay",name:"成员甲税后工资",monthly:15100,stressJob:true,jobPayFraction:0,stability:"受所选情景失业路径影响"}),
    row("incomes",{id:"receipts",name:"成员乙已到账经营净收入",kind:"business",monthly:4800,stability:"按经营回款路径"}),
    row("incomes",{id:"bonus",name:"已存在年度奖金",kind:"bonus",monthly:6000,from:12,every:12,stability:"按期到账"})
  ],
  expenses:[
    row("expenses",{id:"life",name:"生活必要开支",monthly:6000}),
    row("expenses",{id:"care",name:"医疗及照护",kind:"medical",monthly:1100}),
    row("expenses",{id:"flex",name:"可削减开支",kind:"discretionary",monthly:3200}),
    row("expenses",{id:"repair",name:"第18个月突发支出",kind:"emergency",monthly:9000,from:18,to:18,inflationLinked:false})
  ],
  financial:[
    row("financial",{id:"shares",name:"权益组合",value:128000,annualReturn:.025,concentration:.35,fee:.002,settle:1}),
    row("financial",{id:"deposit",name:"六个月后到期存款",kind:"deposit",value:65000,annualReturn:.018,maturity:6}),
    row("financial",{id:"lockfund",name:"限定用途资产",kind:"fund",value:26000,restriction:"restricted",purpose:"指定教育用途，不动用"})
  ],
  properties:[
    row("properties",{id:"home",name:"自住房",city:"示例甲城",type:"住宅",use:"occupied",value:1250000,saleValue:1160000,
      saleLag:5,rent:0,carry:550,saleFee:.025,closingFee:2500,canSell:false}),
    row("properties",{id:"flat",name:"闲置小户型",city:"示例乙城",type:"住宅",value:{low:650000,base:720000,high:780000},
      saleValue:660000,saleLag:4,rent:2500,vacancy:.08,leaseLag:3,discountRent:.10,discountLeaseLag:1,carry:380,saleFee:.028,closingFee:1800})
  ],
  vehicles:[row("vehicles",{id:"car",name:"通勤车",value:76000,saleValue:69000,annualDepreciation:.10,saleLag:1,
    necessary:true,replacementAllowed:true,replacementMonthly:450,carry:920,saleFee:.02,closingFee:400})],
  loans:[
    row("loans",{id:"mort1",name:"自住房贷款",collateral:"home",principal:510000,annualRate:.033,rateType:"floating",resetFirst:12,months:228,
      prepayMin:10000,prepayFee:.002,transferWithLien:false}),
    row("loans",{id:"mort2",name:"闲置房贷款",collateral:"flat",principal:310000,annualRate:.037,rateType:"floating",resetFirst:6,months:204,
      prepayMin:5000,prepayFee:.003,transferWithLien:true}),
    row("loans",{id:"auto",name:"车贷",kind:"car",collateral:"car",principal:33000,annualRate:.045,months:36,
      prepayMin:1000,settlementFee:180,saleMaturityReleaseFee:180,transferWithLien:true})
  ],citySources:[]};
for(const s of paths)E.validateScenario(s);
E.validateHousehold(h);
save("scenarios.json",paths);save("synthetic_household.json",h);
save("loan_input.json",{principal:120000,annual_rate:.042,months:36,input_kind:"synthetic_contract_check"});
