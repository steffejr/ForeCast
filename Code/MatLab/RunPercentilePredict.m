BaseDir = 'C:\Users\Makaye\Desktop\Investment\ForeCast\Data';
cd(BaseDir)
load AMEX_487Stocks_400Days02_16_2012_2010

[NTime NStock] = size(StockClose);
LookBackRange = [5:5:60];
NLB = length(LookBackRange);
TransactionFee = 10;
Money = 1000;
LookBack = 20;
NStock = 50;
Value = zeros(NStock,NLB);

for i = 1:NStock
    for j = 1:NLB
        Stock = flipud((StockClose(:,i)));
        LookBack = LookBackRange(j);
        [Value(i,j)] = subfnPercentile(Stock,LookBack,Money,TransactionFee);
        %[Value, TransactionCosts, SellVector, BuyVector] = subfnPercentile((Stock),LookBack,Money,TransactionFee);
    end
end
% Find which Lookback has the best result for eahc stock
BestValue = max(Value');
BestLB = zeros(NStock,1);
BestReturns = zeros(NStock,1);
for i = 1:NStock
    BestLB(i) = (min(find(Value(i,:) == BestValue(i))));
    BestReturns(i) = Value(i,BestLB(i));
end
%%

figure(2)
plot(Value)
plot(BestReturns)
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