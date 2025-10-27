# Gemfile (repo root)
source "https://rubygems.org"

# GitHub Pages가 jekyll과 호환 플러그인 버전을 관리
gem "github-pages", group: :jekyll_plugins

# Ruby 3.x에서 serve 용
gem "webrick", "~> 1.8"

# 프로젝트에서 고정 사용 중인 의존성
gem "connection_pool", "2.5.0"

# 사이트에서 쓰는 Jekyll 플러그인 목록
group :jekyll_plugins do
  gem "jekyll-archives"        # ⬅️ 버전 제약 제거 (충돌 최소화)
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
  gem "jemoji"
  # 필요시
  # gem "jekyll-include-cache"
  # gem "jekyll-paginate"
end