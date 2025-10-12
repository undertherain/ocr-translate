curl -X 'POST' \
  'http://127.0.0.1:8000/translate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "今日の天気は素晴らしいですね。"
}'