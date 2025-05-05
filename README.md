# tables-agent
`scp -i ~/.ssh/droplet -r ./* root@207.154.206.41:~/notion-agent/`
`docker run -p 8000:8000 -e OPENAI_API_KEY=<Key> -e NOTION_KEY=<Key> notion-agent`