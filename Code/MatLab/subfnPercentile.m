function [Value, TransactionCosts] = subfnPercentile(Stock,LookBack,Money,TransactionFee)
NTime = length(find(Stock>0));

BuyFlag = 1;
SellFlag = 0;
Value = Money;
TransactionCosts = 0;
for j = 1:NTime - (LookBack + 1)
    
    currentData = Stock(j:j+LookBack-1);
    lowPTILE = prctile(currentData,5);
    highPTILE = prctile(currentData,95);
    
    if (Stock(j) > highPTILE) & SellFlag
        % Sell
        BuyFlag = 1;
        SellFlag = 0;
        Value = TotalShares*Stock(j) - TransactionCosts;
        TransactionCosts = TransactionCosts + TransactionFee;
        
    elseif (Stock(j) < lowPTILE) & BuyFlag
        % Buy
        BuyFlag = 0;
        SellFlag = 1;
        TotalShares = (Value - TransactionFee)/Stock(j);
        TransactionCosts = TransactionCosts + TransactionFee;
    end
end
end