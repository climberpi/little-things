data = load('2013.txt');
PaintCnt = max(data(:,1));
ExpertCnt = max([max(data(:,2)), max(data(:,4)), max(data(:,6))]);
Scores = zeros(ExpertCnt, PaintCnt);
for i = 1:PaintCnt
    Scores(data(i,2),data(i,1)) = data(i,3);
    Scores(data(i,4),data(i,1)) = data(i,5);
    Scores(data(i,6),data(i,1)) = data(i,7);
end

Arts = zeros(PaintCnt, PaintCnt);
for i = 1:PaintCnt
    for j = 1:PaintCnt
        entry = 0;
        for k = 1:ExpertCnt
            if Scores(k, i) == 0
                entry += 1;
            elseif Scores(k, j) == 0
                entry += 1;
            else
                entry += Scores(k, i) / Scores(k, j);
            end
        end
        Arts(i, j) = entry;
    end
end

%Modified = diag(1 ./ sum(transpose(Arts))) * Arts;
Modified = Arts * diag(1 ./ sum(Arts));
[eigVector, eigValue] = eig(Modified);
[Result, ID] = sort(abs(eigVector(:,1)), 'descend');
View = zeros(PaintCnt, 5);
for i = 1:PaintCnt
    Cnt = 1;
    View(i, Cnt) = ID(i);
    for j = 1:ExpertCnt
        if Scores(j, ID(i)) != 0
            Cnt = Cnt + 1;
            View(i, Cnt) = Scores(j, ID(i));
        end
    end
    View(i, 5) = 1/3 * (View(i, 2) + View(i, 3) + View(i, 4));
end
View


