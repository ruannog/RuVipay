# 🤝 Contribuindo para o RuViPay

Obrigado por considerar contribuir para o RuViPay! Este documento fornece diretrizes para contribuições.

## 📋 Como Contribuir

### 🐛 Reportando Bugs

1. **Verifique** se o bug já foi reportado nas [Issues](https://github.com/VitorFeuser/RuViPay/issues)
2. **Crie** uma nova issue com:
   - Título claro e descritivo
   - Passos para reproduzir o bug
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)
   - Informações do ambiente (OS, browser, versões)

### ✨ Sugerindo Melhorias

1. **Verifique** se a sugestão já existe nas Issues
2. **Crie** uma nova issue com:
   - Título claro da funcionalidade
   - Descrição detalhada do que você gostaria
   - Por que seria útil
   - Exemplos de uso

### 🔧 Contribuindo com Código

#### **Setup do Ambiente**

```bash
# Fork e clone o repositório
git clone https://github.com/SEU-USERNAME/RuViPay.git
cd RuViPay

# Execute a instalação
./install.sh  # Linux/Mac
# ou
install.bat   # Windows
```

#### **Processo de Desenvolvimento**

1. **Crie** uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. **Faça** suas alterações seguindo os padrões do projeto

3. **Teste** suas alterações:
   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend
   npm test
   ```

4. **Commit** suas mudanças:
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

5. **Push** para sua branch:
   ```bash
   git push origin feature/nome-da-feature
   ```

6. **Abra** um Pull Request

#### **Padrões de Commit**

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação (sem mudança de código)
- `refactor:` Refatoração de código
- `test:` Adição de testes
- `chore:` Tarefas de manutenção

Exemplos:
```
feat: adiciona sistema de metas financeiras
fix: corrige cálculo de saldo no dashboard
docs: atualiza README com novas instruções
```

## 📝 Padrões de Código

### **Python (Backend)**

- Siga PEP 8
- Use type hints
- Docstrings para funções públicas
- Máximo 88 caracteres por linha (Black formatter)

```python
def calculate_balance(income: float, expenses: float) -> float:
    """
    Calcula o saldo baseado em receitas e despesas.
    
    Args:
        income: Total de receitas
        expenses: Total de despesas
        
    Returns:
        Saldo calculado
    """
    return income - expenses
```

### **TypeScript (Frontend)**

- Use TypeScript estrito
- Componentes funcionais com hooks
- Props interfaces bem definidas
- CSS modules ou TailwindCSS

```typescript
interface TransactionProps {
  id: string
  amount: number
  type: 'income' | 'expense'
}

const Transaction: React.FC<TransactionProps> = ({ id, amount, type }) => {
  return (
    <div className="transaction">
      {/* Component content */}
    </div>
  )
}
```

## 🧪 Testes

### **Backend**

```bash
cd backend
pytest tests/ -v --cov=app
```

### **Frontend**

```bash
cd frontend
npm test
npm run test:coverage
```

## 📚 Documentação

- Mantenha o README atualizado
- Documente APIs no código
- Adicione comentários para lógica complexa
- Atualize a documentação da API (OpenAPI/Swagger)

## 🎯 Prioridades de Desenvolvimento

1. **Core Features** - Funcionalidades básicas
2. **UX/UI** - Melhorias na experiência do usuário
3. **Performance** - Otimizações
4. **Testes** - Cobertura de testes
5. **Documentação** - Documentação completa

## 🚀 Roadmap

### **Próximas Versões**

- [ ] Sistema de autenticação completo
- [ ] PWA (Progressive Web App)
- [ ] Relatórios em PDF
- [ ] Integração bancária
- [ ] App mobile
- [ ] Backup automático

## ❓ Dúvidas

Se tiver dúvidas sobre como contribuir:

1. **Leia** a documentação
2. **Procure** nas Issues existentes
3. **Abra** uma nova issue com a tag `question`
4. **Entre em contato** via email: vitor@ruviopay.com

## 🏆 Reconhecimento

Contribuidores serão reconhecidos:

- Nome no README
- Badge de contribuidor
- Menção nas release notes
- Convite para o Discord da comunidade

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [Licença MIT](LICENSE).

---

**Obrigado por contribuir para o RuViPay! 🚀**