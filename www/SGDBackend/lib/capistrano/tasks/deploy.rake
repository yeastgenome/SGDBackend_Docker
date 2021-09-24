namespace :deploy do
  desc 'Build application'
  task :build do
    on roles(:app), in: :sequence do
      execute "export WORKON_HOME=/data/envs/ && source virtualenvwrapper.sh && cd #{current_path} && workon sgd3 && make prod-build"
    end
  end

  desc 'Write config variables'
  task :config do
    on roles(:app), in: :sequence do
      variables = "'"
      ["NEX2_URI", "PREVIEW_SERVER", "PREVIEW_URL", "ARCHIVE_S3_BUCKET", "S3_ACCESS_KEY", "S3_SECRET_KEY", "S3_BUCKET", "EXPRESSION_S3_BUCKET", "GOOGLE_CLIENT_ID", "ES_URI", "ES_INDEX_NAME", "WRITE_ES_URI", "GOOGLE_CAPTCHA_SECRET", "PUSHER_APP_ID", "PUSHER_KEY", "PUSHER_SECRET", "CACHE_URLS", "INPUT_FILE_NAME", "WORKER_LOG_FILE", "SCRIPT_LOG_FILE", "LOG_LEVEL" , "BATTER_URI", "DEFAULT_USER", "MISSING_FILES"].each do |k|
        variables += "export #{k}=\"#{ENV[k]}\"\n"
      end
      variables += "'"
      execute "echo #{variables} > #{current_path}/prod_variables.sh"
    end
  end

  desc 'Restart pyramid'
  task :restart do
    on roles(:app), in: :sequence do
      execute "cd #{current_path} && export WORKON_HOME=/data/envs/ && source virtualenvwrapper.sh && workon sgd3 && . prod_variables.sh && make stop-prod && make run-prod && cat /var/run/pyramid/backend.pid && sleep 4"
    end
  end

  desc 'Index redis'
  task :redis do
    on roles(:app), in: :sequence do
      execute "cd #{current_path} && export WORKON_HOME=/data/envs/ && source virtualenvwrapper.sh && workon sgd3 && . prod_variables.sh && python scripts/disambiguation/create_disambiguation.py && sleep 4"
    end
  end

  desc 'Copy js build'
  task :copy_js do
    on roles(:app), in: :sequence do
      static_source_path = "src/build" 
      static_build_path = "src"
      execute "mkdir -p #{current_path}/#{static_build_path}"
      upload!("./#{static_source_path}", "#{current_path}/#{static_build_path}", { recursive: true })
    end
  end
end
