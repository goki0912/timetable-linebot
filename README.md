# timetable-linebot

乗換案内アプリがうまく使えない祖母のために作った最低限の時刻表LINEbot

LINE公式アカウントを作成してwebhook urlに`https://<デプロイurl>/callback`を登録し、アプリの環境変数にチャネルアクセストークンとチャネルシークレットを設定すれば簡単に利用できます。

実際はapp.pyの時刻表や駅、バス停名を任意のものに変更して運用しています。

デプロイにはfly.ioを利用中

デプロイコマンド `fly deploy -a timetable-linebot`
