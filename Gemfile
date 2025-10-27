# Gemfile (repo 루트)
source "https://rubygems.org"

# GitHub Pages가 Jekyll 및 호환 버전의 플러그인을 관리합니다.
# 주의: 여기서 별도로 'jekyll'을 명시하지 않습니다.
gem "github-pages", group: :jekyll_plugins

# Ruby 3.x에서 로컬 serve에 필요
gem "webrick", "~> 1.8"

# 프로젝트에서 고정 사용 중인 의존성(필요 시 유지)
gem "connection_pool", "2.5.0"

# Jekyll 플러그인(사이트에서 사용하는 것만 유지/추가)
group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-redirect-from"
  gem "jemoji"
  gem "jekyll-archives", "~> 0.16"   # ← 누락되어 빌드 실패 원인
  # (선택) Minimal Mistakes 사용 시 권장
  # gem "jekyll-include-cache"
  # (선택) 사용하는 경우에만
  # gem "jekyll-paginate"
end
