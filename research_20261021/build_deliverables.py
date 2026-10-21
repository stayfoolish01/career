from pathlib import Path
import csv,json,html,hashlib,zipfile
ROOT=Path(__file__).resolve().parent
# ID, area, requirement, priority, evidence, confirmation, acceptance proposal
DATA='''R01|会員|スタディングIDとキャリア会員の対応・登録|P0|S11 S02|認証・同期方式と同意項目|既存・新規で重複せず正しい会員に連携
R02|認証|ログイン・再設定・ロック・セッション|P0|S10 S04|ロック条件と認証移行|再設定後にログインでき旧セッションの扱いが定義される
R03|プロフィール|本人情報・学歴・希望・経験・職歴の編集|P0|S04 S13|必須・選択肢・公開範囲|保存と再表示で入力を維持
R04|資格|資格と等級・科目・合格段階・学習状態|P0|S06 S05|旧ラベルと新マスタの対応|税理士科目と登録済を区別して検索
R05|連携|資格情報の引継ぎと更新|P0|S02 S11|初回コピーか同期か・正本・衝突|再実行しても二重登録されない
R06|求人|求人の項目・資格タグ・掲載主体と種別|P0|S06 S70|直接求人・紹介求人・相談募集|必須応募条件と活かせる資格を区別
R07|検索|勤務地・資格・職種・業種等の複合検索|P0|S06|AND OR・給与換算・並び順|代表条件で期待する求人だけを表示
R08|詳細|求人詳細と掲載期間・更新日|P0|S70|期限切れ求人の扱い|非公開求人へ応募できない
R09|キープ|求人キープ・リスト|P1|S04 S70|匿名時保持・ログイン統合|追加解除と一覧が一致
R10|応募|応募・自己アピール・応募先情報|P0|S04 S03|初回制限・二重送信・必須書類|連打や再送で意図しない二重応募がない
R11|履歴|応募履歴・辞退連絡・再応募|P0|S04|状態モデル・再応募単位|再応募を過去応募と識別して追跡
R12|書類|アップロードと応募先ごとの差し替え|P0|S04|形式・容量・共通書類との関係|別応募先に提出書類が混ざらない
R13|メッセージ|相手別メッセージ・既読未読・添付|P0|S04|初回送信制限・削除・保持|関係者以外にスレッドを表示しない
R14|通知|返信・未読・スカウト通知と配信設定|P0|S04|必須通知・停止条件・配信基盤|旧停止設定を守り通知を重複しない
R15|公開制御|匿名検索と応募・返信時の開示|P0|S04|自由記述・添付・相談経由の例外|未接触時に氏名と生年月日を表示しない
R16|ブロック|法人検索・ブロックと解除|P0|S04|非掲載法人・過去接触・法人統合|ブロック先の検索・詳細・送信を制御
R17|スカウト|候補者検索・送信・受信・返信|P0|S05 S13|検索条件・送信上限・求人紐づけ|返信相手にのみ定義した情報を開示
R18|スカウト枠|月次付与・消費・失効・繰越不可|P0|S05|付与数・境界時刻・失敗時返却|月末翌月と同時送信でも残数整合
R19|法人|法人申込審査・アカウント発行|P0|S05|審査内容・停止・企業と紹介事業者|未承認法人が候補者を閲覧できない
R20|権限|法人内担当者と運営の権限|P0|S05|ロール・グループ・運営参照権限|別法人や退職担当者のアクセスを拒否
R21|審査|求人登録・編集・審査・公開停止|P0|S05|承認者・差戻し・更新時再審査|審査未完了の原稿を公開しない
R22|成果|採用・入社・年収・紹介進捗の報告|P0|S08 S05|成果帰属・申告者・証憑|既存選考と新規応募の成果を区別
R23|請求|契約別の成功報酬・請求台帳|P0|S05 S08|報酬率・請求時期・返金|入社成果から適用契約と金額を追跡
R24|相談|運営相談の申込・予約・面談・紹介|P1|S14 S69|予約基盤・503復旧後の項目|予約結果と面談担当を引継げる
R25|エージェント|提携一覧・得意業界職種・詳細・相談|P1|S07 S22 S66|法人とブランド・相談募集の対応|紹介ページから正しい相談先に進む
R26|コンテンツ|記事・動画・会員限定閲覧|P1|S01 S03|CMS・動画原本・会員権限|限定動画へ未会員が直接アクセス不可
R27|問い合わせ|個人・法人フォームと対応管理|P1|S15 S16|分類・担当・通知・営業連携|必要情報と同意を保存し対応先へ渡す
R28|督促|5営業日返信ルールと運営対応|P1|S04|自動化の要否・休日・対象案件|未返信対象の抽出と対応履歴を追跡
R29|退会|退会・停止・保持・削除|P0|S08 S12|学習会員への影響・相手側履歴|退会者の公開停止と保持条件を検証
R30|移行|全件・差分移行とID・添付照合|P0|提案|旧DB仕様・取得期限・対象範囲|件数・外部キー・添付・ブロックを照合
R31|SEO|旧URLと流入ページの維持・転送|P1|S01 S20 S21|旧URL一覧・ドメイン・終了求人|重要流入URLが適切な新ページへ到達
R32|監査|情報開示・閲覧・運営操作の記録|P0|提案|記録項目・権限・保存期限|開示相手と操作主体を追跡できる
R33|運用|監視・バックアップ・復旧・連携再処理|P0|提案|可用性・RTO RPO・責任者|復元と再処理で応募・通知を重複しない
R34|集計|登録・応募・返信・面談・入社の計測|P1|提案|KPI・イベント・個人情報最小化|各段階の件数と定義が照合可能
R35|改善|辞退ボタンと選考状態の明示|P2|提案 S04|現行メッセージ運用の置換可否|求職者と採用側の状態が食い違わない
R36|改善|応募済みへの重複スカウト抑制|P2|提案 S04|匿名性と照合権限|匿名情報を増やさず重複を抑制
R37|性能|実利用量に基づく検索・応募の性能|P0|提案|実件数・ピーク・応答時間目標|合意した負荷で測定し達成
R38|端末|スマートフォンでの主要操作|P0|S03|対象OS・ブラウザ・添付|検索から応募と返信まで実端末確認'''
with (ROOT/'requirements.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID','領域','要件候補','優先度案','根拠','社内確認事項','受入確認案'])
    for line in DATA.splitlines():w.writerow(line.split('|'))
rows=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
links=''.join('<tr><td>'+html.escape(r['id'])+'</td><td>'+html.escape(str(r.get('status','未取得')))+'</td><td>'+html.escape(r.get('title',''))+'</td><td><a href="'+html.escape(r['url'],quote=True)+'">原URL</a></td><td>'+ ('<a href="sources/'+r['id']+'.txt">保存本文</a> / <a href="sources/'+r['id']+'.html">保存HTML</a>' if (ROOT/'sources'/f"{r['id']}.txt").exists() else html.escape(r.get('error','')))+'</td></tr>' for r in rows)
(ROOT/'index.html').write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><title>スタディングキャリア 保存資料索引</title><style>body{font:16px/1.7 sans-serif;margin:32px;max-width:1400px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px}a{color:#1261a0}</style><h1>スタディングキャリア 保存資料索引</h1><p>2026年10月21日調査。原文参照には保存本文を使用。HTMLの画像・CSS・リンクは外部に依存します。完全なサイトバックアップではありません。</p><p><a href="要件定義の基礎調査.md">調査報告</a> / <a href="requirements.csv">要件候補38件</a> / <a href="sources.csv">出典台帳</a> / <a href="form_fields.csv">入力項目</a> / <a href="assets_manifest.json">画像取得結果</a></p><table><tr><th>ID</th><th>HTTP</th><th>ページ</th><th>出典</th><th>保存先</th></tr>'+links+'</table></html>',encoding='utf-8')
# Check archive integrity before packaging.
for r in rows:
    if r.get('sha256'):
        assert hashlib.sha256((ROOT/'sources'/f"{r['id']}.html").read_bytes()).hexdigest()==r['sha256']
assert len(DATA.splitlines())==38
with zipfile.ZipFile(ROOT.parent/'STキャリア_再構築調査_20261021.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT.parent))
print(json.dumps({'requirements':38,'source_attempts':len(rows),'http200':sum(r.get('status')==200 for r in rows),'agent_pages':sum('/column/agent/' in r['url'] for r in rows),'archive_integrity':'passed'},ensure_ascii=False))
