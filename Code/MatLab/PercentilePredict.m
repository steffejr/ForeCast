sClose = close;
clear close

[NTime NStock] = size(sClose);
LookBackRange = 50;
NLB = length(LookBackRange);

TransactionCost = 10;
Money = 1000;
TotalValue = zeros(NStock,NLB);
TotalShares = zeros(NStock,NLB);
TotalTransactions = zeros(NStock,NLB);
for i = 1:NStock
    for k = NLB:-1:1
        BuyFlag = 1; % Ready to Buy
        SellFlag = 0; % NOT Ready to Sell
        TotalValue(i,k) = Money;
        for j = 1:NTime - (LookBackRange(k) + 1)
           
            currentData = sClose(j:j+LookBackRange(k)-1,i);
            lowPTILE = prctile(currentData,5);
            highPTILE = prctile(currentData,95);
            medianPTILE=prctile(currentData,50);
           
            %if (sClose(j) > highPTILE) & SellFlag
            if (sClose(j) > medianPTILE)  &&  SellFlag
                % Sell
                BuyFlag = 1;
                SellFlag = 0;
                TotalValue(i,k) = TotalShares(i,k)*sClose(j,i) - TransactionCost;
                TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
               
            elseif (sClose(j) < lowPTILE) & BuyFlag
                % Buy
                BuyFlag = 0;
                SellFlag = 1;
                underFlag = 1;
                TotalShares(i,k) = (TotalValue(i,k) - TransactionCost)/sClose(j,i);
                TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
            end
        end
    end
end