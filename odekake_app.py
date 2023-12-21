import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe

st.set_page_config(layout="wide")

# カスタムスタイルを適用するためのCSS
st.markdown("""
<style>
.centered {
    text-align: center;
}
.stCheckbox {
    margin-top: 2.7em;
    margin-bottom: -2.945em;
}
</style>
""", unsafe_allow_html=True)


# タイトルを中央に配置するためのカスタムクラスを使用
st.markdown('<h1 class="centered">休日お出かけAPP</h1>', unsafe_allow_html=True)

# 認証のために機能役割を決めるアクセス先をscopesに設定
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Google Sheets APIの認証情報を指定
credentials = Credentials.from_service_account_file(
    'service_account.json',
    scopes=scopes
)

# 認証情報を格納しているcredentialsを使って、gspread.authorizeでスプレッドシートの使用許可を取り、
# その認証結果をgcに代入
gc = gspread.authorize(credentials)

# 使用するスプレッドシートのアクセス先をSP_SHEET_KEYに代入
# https://docs.google.com/spreadsheets/d/「ここの部分がSP_SHEET_KEYに代入される」
SP_SHEET_KEY = '1w62VeFTUw_5onAtRjaaDevIllqm9oV1k03-VLcoP6_E'

# 開きたいスプレッドシートを認証結果を格納したgcを使ってgc.open_by_keyで開く
sh = gc.open_by_key(SP_SHEET_KEY)

# Google Sheetsのシート名
SP_SHEET = '家族会話メモ'

# gc.open_by_keyで開いたスプレッドシートのsampleシートをsh.worksheet(SP_SHEET)で情報を得て、worksheetに代入する
worksheet = sh.worksheet(SP_SHEET)

# サイドバー：タイトルとして表示
st.sidebar.write("家族会話メモ")

# サイドバー：家族会話メモの"Who"
family_who = st.sidebar.multiselect(
    "誰のメモ？",
    ["パパ", "ママ", "娘"]
)

# サイドバー：行きたい場所・したいこと
family_memo = st.sidebar.text_input("行きたい場所・したいこと")

# サイドバー：追加ボタンの設置
if st.sidebar.button("追加"):
    # スプレッドシートのワークシートを開く
    sheet = gc.open_by_key(SP_SHEET_KEY).worksheet("家族会話メモ")

    # データをスプレッドシートに追加
    who_str = ', '.join(map(str, family_who))  # family_whoを文字列に変換
    row = [who_str, str(family_memo)]
    sheet.append_row(row)
    
# タイトルとして表示
#st.header("家族会話メモ")

# スプレッドシートから指定したシートのデータを取得
#worksheet = sh.worksheet(SP_SHEET)
#data = worksheet.get_all_values()

# テーブルとして表示
#st.table(data)


# 等分で分割
col1, col2 = st.columns(2)
# 左右を 1:1 で分割、分割の幅を大きく
col1, col2 = st.columns([1, 1], gap='large')

with col1:
    st.header('家族会話メモ')
    df5 = gc.open_by_key(SP_SHEET_KEY).worksheet("家族会話メモ")
    # スプレッドシートから全てのレコードを取得
    records = df5.get_all_values()

    # レコードをPandasのDataFrameに変換
    df5 = pd.DataFrame(records)
    
    col9, col10 = st.columns([1, 50]) 
    checkbox_values = [False] * len(df5)
    with col9:
        for i in range(len(df5)):
         checkbox_values[i] = st.checkbox("", key=f"checkbox5_{i}")
    df5['選択'] = checkbox_values
    selected_rows5 = df5[df5['選択'] == True]
    with col10:
         st.dataframe(df5, height=300)

with col2:
    st.header('お出かけ履歴')
    df6 = gc.open_by_key(SP_SHEET_KEY).worksheet("おでかけ履歴")
    records = df6.get_all_values()
    df6 = pd.DataFrame(records)    
    
    col11, col12 = st.columns([1, 50]) 
    checkbox_values = [False] * len(df6)
    with col11:
        for i in range(len(df6)):
         checkbox_values[i] = st.checkbox("", key=f"checkbox6_{i}")
    df6['選択'] = checkbox_values
    selected_rows6 = df6[df6['選択'] == True]
    with col12:
         st.dataframe(df6, height=300)


st.header('週末地区イベント')
df = gc.open_by_key(SP_SHEET_KEY).worksheet("週末地区イベント")
records = df.get_all_values()
df = pd.DataFrame(records)

# カラムを2つ作成します。1つはDataFrame用、もう1つはチェックボックス用です。
col1, col2 = st.columns([1, 50]) # 比率を調整することで、各カラムの幅を変更できます。
# チェックボックスの状態を保持するリストを作成します。
checkbox_values = [False] * len(df)
# 1つ目のカラムでチェックボックスを表示します。
with col1:
    for i in range(len(df)):
        # チェックボックスの状態を更新します。
        checkbox_values[i] = st.checkbox("", key=f"checkbox1_{i}")
# 選択された行のみをフィルタリングするために、選択状態をDataFrameに適用します。
df['選択'] = checkbox_values
selected_rows1 = df[df['選択'] == True]

# 2つ目のカラムでDataFrameを表示します。
with col2:
    st.dataframe(df)


st.header('お出かけスポットランキング')
df2 = gc.open_by_key(SP_SHEET_KEY).worksheet("お出かけスポットランキング")
records = df2.get_all_values()
df2 = pd.DataFrame(records)

col3, col4 = st.columns([1, 50]) 
checkbox_values = [False] * len(df2)
with col3:
    for i in range(len(df2)):
        checkbox_values[i] = st.checkbox("", key=f"checkbox2_{i}")
df2['選択'] = checkbox_values
selected_rows2 = df2[df2['選択'] == True]
with col4:
    st.dataframe(df2, height=1900)

st.header('直近お出かけトピックス')
df3 = gc.open_by_key(SP_SHEET_KEY).worksheet("大阪府_直近お出かけトピックス")
records = df3.get_all_values()
df3 = pd.DataFrame(records)
col5, col6 = st.columns([1, 50]) 
checkbox_values = [False] * len(df3)
with col5:
    for i in range(len(df3)):
        checkbox_values[i] = st.checkbox("", key=f"checkbox3_{i}")
df3['選択'] = checkbox_values
selected_rows3 = df3[df3['選択'] == True]
with col6:
    st.dataframe(df3, height=2300)

st.header('直近グルメトピックス')
df4 = gc.open_by_key(SP_SHEET_KEY).worksheet("大阪府_直近グルメトピックス")
records = df4.get_all_values()
df4 = pd.DataFrame(records)
col7, col8 = st.columns([1, 50]) 
checkbox_values = [False] * len(df4)
with col7:
    for i in range(len(df4)):
        checkbox_values[i] = st.checkbox("", key=f"checkbox4_{i}")
df4['選択'] = checkbox_values
selected_rows4 = df4[df4['選択'] == True]
with col8:
    st.dataframe(df4, height=2300)


st.markdown("<h1 style='text-align: center;'>今週のお出かけ候補一覧</h1>", unsafe_allow_html=True)


# 選択された行を表示する（家族会話メモ）
if not selected_rows5.empty:
    st.write(selected_rows5)
# 選択された行を表示する（お出かけ履歴）
if not selected_rows6.empty:
    st.write(selected_rows6) 
# 選択された行を表示する（週末地区イベント）
if not selected_rows1.empty:
    st.write(selected_rows1)
# 選択された行を表示する（お出かけスポットランキング）
if not selected_rows2.empty:
    st.write(selected_rows2)
# 選択された行を表示する（直近お出かけトピックス）
if not selected_rows3.empty:
    st.write(selected_rows3)
# 選択された行を表示する（直近グルメトピックス）
if not selected_rows4.empty:
    st.write(selected_rows4)