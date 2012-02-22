sClose = close;
clear close

[NTime NStock] = size(sClose);

%sClose=sClose(NTime:-1:1,:);    %%% not sure about temporal ordering, 

LookBackRange = 40;
NLB = length(LookBackRange);

TransactionCost = 10;
Money = 1000;    %%% every stock starts with 1000, but no prior share ownership, buying-in is required
TotalValue = zeros(NStock,NLB);
TotalShares = zeros(NStock,NLB);
TotalTransactions = zeros(NStock,NLB);
ActionBool=zeros(NTime,NStock); % boolean flag to find out whether some trading takes place, for realism computation
%%
for i = 1:1%NStock
    for k = NLB:-1:1
        
                
        BuyFlag = 0;   %Flags of what happened LAST: if both are zero, then trade has closed;  if one is unequal to zero, trade is open
        SellFlag = 0;
        TotalValue(i,k) = Money;

        for j = 1:NTime - (LookBackRange(k) + 1)
           
            currentData = sClose(j:j+LookBackRange(k)-1,i);
            lowPTILE = prctile(currentData,10);
            highPTILE = prctile(currentData,90);
            medianPTILE=prctile(currentData,50);
           
            % This condition should never be met because you need to but
            % before you can sell
%             if (sClose(j,i) > highPTILE) && (SellFlag==0 && BuyFlag==0)
%                 
%                     % Sell to open
%                     fprintf(1,'Sell to open\n')
%                     if TotalShares(i,k)>0   %% make sure first ever opening cannot be SELLING, since no shares are owned yet
%                     
%                         SellFlag = 1;
%                         TotalValue(i,k) = TotalValue(i,k) + TotalShares(i,k)*sClose(j,i) - TransactionCost;
%                         TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
%                         TotalShares(i,k) = 0;
%                         ActionBool(j,i)=1;  
%                     
%                     end
               
            if (sClose(j) < lowPTILE) && (SellFlag==0 && BuyFlag==0)
                % Price is too low so buy.
                    % Buy to open
                    
                    if sClose(j,i)~=0   %%% make sure price is not zero
                        BuyFlag = 1;
                        TotalShares(i,k) = floor( (TotalValue(i,k) - TransactionCost)/sClose(j,i) );  % rounded down for realism
                        % The transaction cost is already accounted for in
                        % the total number of shares
                        % TotalValue(i,k) = TotalValue(i,k)-TotalShares(i,k)*sClose(j,i) -TransactionCost;
                        TotalValue(i,k) = TotalValue(i,k)-TotalShares(i,k)*sClose(j,i);
                        TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
                        ActionBool(j,i)=1;
                        fprintf(1,'Buy %d shares at $%0.2f, for $%0.2f\n',TotalShares(i,k),sClose(j,i),TotalShares(i,k)*sClose(j,i));
                    end
                    
                    
              elseif (sClose(j) > medianPTILE)  &&  BuyFlag
                  % Price has returned to the median, sell
                    % Sell to close
                    SellFlag = 0;
                    BuyFlag = 0;
                    TotalValue(i,k) = TotalValue(i,k) + TotalShares(i,k)*sClose(j,i) - TransactionCost;
                    TotalShares(i,k) = 0 ;
                    TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
                    ActionBool(j,i)=1;  
                    fprintf(1,'Sell %d shares at $%0.2f, for $0.2f\n,',TotalShares(i,k),sClose(j,i),TotalShares(i,k)*sClose(j,i) - TransactionCost);
              
%             elseif (sClose(j) < medianPTILE)  &&  SellFlag
%                     % Buy to close
%                     if sClose(j,i)~=0
%                         BuyFlag = 0;
%                         SellFlag = 0;
%                         TotalShares(i,k) = floor( (TotalValue(i,k) - TransactionCost)/sClose(j,i) );
%                         TotalValue(i,k) = TotalValue(i,k)-TotalShares(i,k)*sClose(j,i) -TransactionCost;
%                         TotalTransactions(i,k) = TotalTransactions(i,k) + TransactionCost;
%                         ActionBool(j,i)=1;
%                     end
%                 
            end
            
                       
        end
       % keyboard;
    end
end