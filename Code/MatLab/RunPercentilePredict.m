BaseDir = 'C:\Users\Makaye\Desktop\Investment\ForeCast\Data';
cd(BaseDir)
load AMEX_487Stocks_400Days02_16_2012_2010

[NTime NStock] = size(StockClose);
LookBackRange = 40;
NLB = length(LookBackRange);
TransactionFee = 10;
Money = 1000;
LookBack = 20;

Value = zeros(NStock,NLB);

for i = 1:NStock
    for j = 1:NLB
        Stock = flipud((StockClose(:,i)));
        LookBack = LookBackRange(j);
        [Value(i,j)] = subfnPercentile(Stock,LookBack,Money,TransactionFee);
        %[Value, TransactionCosts, SellVector, BuyVector] = subfnPercentile((Stock),LookBack,Money,TransactionFee);
    end
end
%%
figure(2)
plot(Value)
%% Figure
index = 3;
Name = StockList(index,:);
Stock = flipud(StockClose(:,index));
[V, TransactionCosts, SellVector, BuyVector] = subfnPercentile((Stock),40,Money,TransactionFee);
V
figure(1)
clf
hold on
plot(Stock)
plot(BuyVector,'o')
plot(SellVector,'xr')
title(Name)