function subfnFindMostLow(StockClose,LookBack)
NStock = size(AllStock,2);
PercentAbove = zeros(NStock,1);
for i = 1:NStock
    Stock = flipud((StockClose(:,i)));

    lowPercentile(i) = prctile(AllStock(:,i),5);
    medianPercentile(i) = prctile(AllStock(:,i),50);
    PercentAbove(i) = (Stock(end-1) - medianPercentile(i))/medianPercentile(i);
end
    


