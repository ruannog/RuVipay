# 🚀 RuViPay - Comandos para Subir no GitHub

## 📋 Pré-requisitos
- Git instalado
- Conta no GitHub
- Repositório criado no GitHub (público ou privado)

## 🔧 Configuração Inicial (Execute apenas uma vez)

### 1. Configurar Git globalmente (se ainda não configurou)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@gmail.com"
```

### 2. Navegar para o diretório do projeto
```bash
cd "c:\Users\ruanb\OneDrive\Área de Trabalho\ruviopay"
```

## 🚀 Upload para GitHub

### 3. Inicializar repositório Git (se ainda não foi feito)
```bash
git init
```

### 4. Adicionar remote do GitHub
```bash
# Substitua YOUR-USERNAME pelo seu usuário do GitHub
git remote add origin https://github.com/VitorFeuser/RuViPay.git

# Ou se preferir SSH (recomendado)
git remote add origin git@github.com:VitorFeuser/RuViPay.git
```

### 5. Verificar arquivos que serão commitados
```bash
git status
```

### 6. Adicionar todos os arquivos
```bash
git add .
```

### 7. Fazer o primeiro commit
```bash
git commit -m "🚀 feat: implementa sistema completo RuViPay

- ⚛️ Frontend React com TypeScript e TailwindCSS
- 🐍 Backend FastAPI com SQLAlchemy
- 📊 Dashboard interativo com Chart.js
- 💰 CRUD completo de transações e categorias
- 🔗 Integração Frontend-Backend via React Query
- 🎨 Interface responsiva e moderna
- 📚 Documentação completa
- 🐳 Configuração Docker
- 🔧 Scripts de instalação automática
- ✅ Sistema de autenticação
- 📈 Gráficos e relatórios financeiros"
```

### 8. Configurar branch principal
```bash
git branch -M main
```

### 9. Fazer o push inicial
```bash
# Primeira vez - força o push
git push -u origin main --force

# Das próximas vezes, apenas:
git push
```

## 🔄 Comandos para Updates Futuros

### Após fazer mudanças no código:
```bash
# Ver o que mudou
git status

# Adicionar arquivos específicos
git add frontend/src/components/NewComponent.tsx
git add backend/app/api/new_endpoint.py

# Ou adicionar tudo
git add .

# Commit com mensagem descritiva
git commit -m "feat: adiciona nova funcionalidade X"

# Push para GitHub
git push
```

## 📝 Padrões de Commit

Use mensagens claras e descritivas:

```bash
# Nova funcionalidade
git commit -m "feat: adiciona sistema de metas financeiras"

# Correção de bug
git commit -m "fix: corrige cálculo de saldo no dashboard"

# Atualização de documentação
git commit -m "docs: atualiza README com instruções de deploy"

# Refatoração
git commit -m "refactor: melhora estrutura do componente Dashboard"

# Melhorias de estilo
git commit -m "style: aplica formatação consistente no código"
```

## 🏷️ Criando Releases

### Para criar uma versão/release:
```bash
# Criar tag
git tag -a v1.0.0 -m "🎉 Release v1.0.0 - Sistema RuViPay completo"

# Push da tag
git push origin v1.0.0

# Ou push de todas as tags
git push --tags
```

## 🔧 Comandos Úteis

### Verificar status
```bash
git status
git log --oneline
```

### Desfazer mudanças
```bash
# Desfazer mudanças não commitadas
git checkout .

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Ver diferenças
git diff
```

### Sincronizar com GitHub
```bash
# Buscar mudanças do GitHub
git fetch origin

# Merge das mudanças
git merge origin/main

# Ou pull (fetch + merge)
git pull origin main
```

## 🚀 URLs Finais

Após o upload, seu projeto estará disponível em:

- **🌐 Repositório**: https://github.com/VitorFeuser/RuViPay
- **📚 README**: https://github.com/VitorFeuser/RuViPay#readme
- **🐛 Issues**: https://github.com/VitorFeuser/RuViPay/issues
- **📋 Projects**: https://github.com/VitorFeuser/RuViPay/projects
- **⚙️ Actions**: https://github.com/VitorFeuser/RuViPay/actions

## 🎯 Próximos Passos

1. **🔧 Configure GitHub Pages** para demo online
2. **🤖 Configure GitHub Actions** para CI/CD
3. **📊 Adicione badges** no README
4. **🏷️ Crie milestones** para organizar desenvolvimento
5. **👥 Convide colaboradores** se necessário

---

**🎉 Pronto! Seu projeto RuViPay estará no GitHub e disponível para o mundo!**