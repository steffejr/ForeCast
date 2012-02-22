function [Value, TransactionCosts, SellVector, BuyVector] = subfnPercentile(Stock,LookBack,Money,TransactionFee)
NTime = length(find(Stock>0));

BuyFlag = 1; % Ready to Buy
SellFlag = 0; % NOT Ready to Sell
Value = Money;
TransactionCosts = 0;

BuyVector = zeros(NTime,1);
SellVector = zeros(NTime,1);
% Assume that index value 1 is the OLDEST time point
%fprintf(1,'=======================\n')
for j = LookBack : NTime
%for j = 1:NTime - (LookBack + 1)
    
    currentData = Stock(j-LookBack+1:j);
    lowPTILE = prctile(currentData,5);
    highPTILE = prctile(currentData,95);
    medianPTILE=prctile(currentData,50);
    
    % Sell when the Stock returns to the median value
    if (Stock(j) > highPTILE) & SellFlag
        % Sell
        SellVector(j) = Stock(j);
        BuyFlag = 1;
        SellFlag = 0;
        Value = TotalShares*Stock(j) - TransactionCosts;
        TransactionCosts = TransactionCosts + TransactionFee;
        %fprintf(1,'Sell: $%0.2f at %0.2f\n',Value,Stock(j));
        
    elseif (Stock(j) < lowPTILE) & BuyFlag
        % Buy
        BuyVector(j) = Stock(j);
        BuyFlag = 0;
        SellFlag = 1;
        TotalShares = floor((Value - TransactionFee)/Stock(j));
        TransactionCosts = TransactionCosts + TransactionFee;
        %fprintf(1,'Buy: %d shares at %0.2f for a value of $%0.2f\n',TotalShares, Stock(j),TotalShares*Stock(j));
    end
end
