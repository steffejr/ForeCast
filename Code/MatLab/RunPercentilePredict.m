
[NTime NStock] = size(sClose);
LookBackRange = 40;
NLB = length(LookBackRange);
TransactionFee = 10;
Money = 1000;
LookBack = 20;

Value = zeros(NStock,NLB);

for i = 1:NStock
    for j = 1:NLB
        Stock = sClose(:,i);
        LookBack = LookBackRange(j);
        [Value(i,j)] = subfnPercentile(Stock,LookBack,Money,TransactionFee);
    end
end

