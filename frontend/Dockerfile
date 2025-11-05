FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

# 必要な依存関係をクリーンインストール
RUN npm install

COPY . .

# viteのデフォルトポートを明示的に指定
EXPOSE 5173

# viteのパスを明示的に追加
ENV PATH /app/node_modules/.bin:$PATH

CMD ["npm", "run", "dev", "--", "--host"]