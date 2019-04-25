# NumberPlaceSolver
簡単に言うと，SATソルバーをラップして，数独を楽に解けるようにした数独専用ソルバー

詳細は以下に載ってあるらしい．

https://qiita.com/okmt1230z/items/63f49e021c94077c343e

プログラムは以下のようにして数独の解を求めています．

1. Encording : txtファイルの数独情報からcnfファイルを作る
2. Solving : システムコールでSATソルバー clasp を起動してcnfファイルを解く
3. Decording : clasp のログを解析して，数独の答えを表示する

9x9,16x16,(多分25x25やそれ以上の)の数独が解けることを確認しました．
プログラムを実行したら，解きたい問題ファイルの入力を求められますので，ファイル名を入力してください．(懇願)

構成
numpre_solver.py : 数独ソルバー
toi_001.txt : 9x9の数独の問題ファイル
toi_002.txt : 16x16の数独の問題ファイル
toi_001.cnf : toi_001.txtのcnfファイル(プログラムを実行すると自動生成される)
toi_001.cnf : toi_002.txtのcnfファイル(プログラムを実行すると自動生成される)
sample.cnf : cnfのsample(SATソルバーが動くかどうかお試しください)
sample.log : sample.cnfをSATソルバーclasp3.3.4で実行したログ
