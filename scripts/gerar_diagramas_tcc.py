"""
Gerador de Diagramas para TCC - RuViPay
Gera todos os diagramas necessários para documentação acadêmica
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from pathlib import Path

def criar_diagrama_classes():
    """Cria o Diagrama de Classes UML"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Cores
    cor_classe = '#E3F2FD'
    cor_borda = '#1976D2'
    
    # Classe User
    user_box = FancyBboxPatch(
        (0.5, 7), 2.5, 2.5,
        boxstyle="round,pad=0.1",
        facecolor=cor_classe,
        edgecolor=cor_borda,
        linewidth=2
    )
    ax.add_patch(user_box)
    
    ax.text(1.75, 9, 'User', fontsize=14, fontweight='bold', ha='center')
    ax.text(1.75, 8.5, '─' * 25, fontsize=10, ha='center')
    user_attrs = [
        '+ id: Integer (PK)',
        '+ username: String',
        '+ email: String',
        '+ full_name: String',
        '+ hashed_password: String',
        '+ is_active: Boolean',
        '+ created_at: DateTime',
        '+ updated_at: DateTime'
    ]
    for i, attr in enumerate(user_attrs):
        ax.text(0.7, 8.3 - i*0.15, attr, fontsize=9, va='center')
    
    # Classe Category  
    category_box = FancyBboxPatch(
        (4, 7), 2.5, 2.5,
        boxstyle="round,pad=0.1",
        facecolor=cor_classe,
        edgecolor=cor_borda,
        linewidth=2
    )
    ax.add_patch(category_box)
    
    ax.text(5.25, 9, 'Category', fontsize=14, fontweight='bold', ha='center')
    ax.text(5.25, 8.5, '─' * 25, fontsize=10, ha='center')
    category_attrs = [
        '+ id: Integer (PK)',
        '+ name: String',
        '+ description: String',
        '+ type: String',
        '+ color: String',
        '+ icon: String',
        '+ is_active: Boolean',
        '+ user_id: Integer (FK)'
    ]
    for i, attr in enumerate(category_attrs):
        ax.text(4.2, 8.3 - i*0.15, attr, fontsize=9, va='center')
    
    # Classe Transaction
    transaction_box = FancyBboxPatch(
        (2, 3.5), 3, 2.5,
        boxstyle="round,pad=0.1",
        facecolor=cor_classe,
        edgecolor=cor_borda,
        linewidth=2
    )
    ax.add_patch(transaction_box)
    
    ax.text(3.5, 5.5, 'Transaction', fontsize=14, fontweight='bold', ha='center')
    ax.text(3.5, 5, '─' * 30, fontsize=10, ha='center')
    transaction_attrs = [
        '+ id: Integer (PK)',
        '+ description: String',
        '+ amount: Decimal',
        '+ type: String',
        '+ date: DateTime',
        '+ notes: Text',
        '+ user_id: Integer (FK)',
        '+ category_id: Integer (FK)'
    ]
    for i, attr in enumerate(transaction_attrs):
        ax.text(2.2, 4.8 - i*0.15, attr, fontsize=9, va='center')
    
    # Relacionamentos
    # User -> Category (1:N)
    ax.annotate('', xy=(4, 8), xytext=(3, 8),
                arrowprops=dict(arrowstyle='->', lw=2, color=cor_borda))
    ax.text(3.5, 8.2, '1:N', fontsize=10, ha='center', fontweight='bold')
    ax.text(3.5, 7.8, 'possui', fontsize=9, ha='center', style='italic')
    
    # User -> Transaction (1:N)
    ax.annotate('', xy=(2.5, 6), xytext=(2, 7),
                arrowprops=dict(arrowstyle='->', lw=2, color=cor_borda))
    ax.text(1.8, 6.5, '1:N', fontsize=10, ha='center', fontweight='bold')
    ax.text(1.5, 6.2, 'realiza', fontsize=9, ha='center', style='italic')
    
    # Category -> Transaction (1:N)
    ax.annotate('', xy=(4.5, 6), xytext=(5, 7),
                arrowprops=dict(arrowstyle='->', lw=2, color=cor_borda))
    ax.text(5.2, 6.5, '1:N', fontsize=10, ha='center', fontweight='bold')
    ax.text(5.5, 6.2, 'classifica', fontsize=9, ha='center', style='italic')
    
    # Título
    ax.text(5, 9.7, 'DIAGRAMA DE CLASSES - RuViPay', fontsize=18, fontweight='bold', ha='center')
    ax.text(5, 9.4, 'Sistema de Gestão Financeira Pessoal', fontsize=12, ha='center', style='italic')
    
    # Legenda
    ax.text(7.5, 2, 'LEGENDA:', fontsize=12, fontweight='bold')
    ax.text(7.5, 1.7, 'PK = Primary Key', fontsize=10)
    ax.text(7.5, 1.5, 'FK = Foreign Key', fontsize=10)
    ax.text(7.5, 1.3, '1:N = Um para Muitos', fontsize=10)
    
    plt.tight_layout()
    return fig

def criar_mer_der():
    """Cria o Modelo Entidade-Relacionamento (MER/DER)"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Cores
    cor_entidade = '#FFF3E0'
    cor_relacionamento = '#E8F5E8'
    cor_borda = '#F57C00'
    cor_rel_borda = '#4CAF50'
    
    # Entidade USER
    user_rect = mpatches.Rectangle((1, 6), 2, 1.5, facecolor=cor_entidade, edgecolor=cor_borda, linewidth=2)
    ax.add_patch(user_rect)
    ax.text(2, 6.75, 'USER', fontsize=14, fontweight='bold', ha='center')
    
    # Entidade CATEGORY
    category_rect = mpatches.Rectangle((6, 6), 2, 1.5, facecolor=cor_entidade, edgecolor=cor_borda, linewidth=2)
    ax.add_patch(category_rect)
    ax.text(7, 6.75, 'CATEGORY', fontsize=14, fontweight='bold', ha='center')
    
    # Entidade TRANSACTION
    transaction_rect = mpatches.Rectangle((3.5, 2), 2, 1.5, facecolor=cor_entidade, edgecolor=cor_borda, linewidth=2)
    ax.add_patch(transaction_rect)
    ax.text(4.5, 2.75, 'TRANSACTION', fontsize=14, fontweight='bold', ha='center')
    
    # Relacionamento POSSUI (User -> Category)
    possui_diamond = mpatches.RegularPolygon((4.5, 6.75), 4, radius=0.5, 
                                           facecolor=cor_relacionamento, edgecolor=cor_rel_borda, linewidth=2)
    ax.add_patch(possui_diamond)
    ax.text(4.5, 6.75, 'POSSUI', fontsize=10, fontweight='bold', ha='center')
    
    # Relacionamento REALIZA (User -> Transaction)
    realiza_diamond = mpatches.RegularPolygon((2.5, 4.5), 4, radius=0.5,
                                            facecolor=cor_relacionamento, edgecolor=cor_rel_borda, linewidth=2)
    ax.add_patch(realiza_diamond)
    ax.text(2.5, 4.5, 'REALIZA', fontsize=9, fontweight='bold', ha='center')
    
    # Relacionamento PERTENCE (Transaction -> Category)  
    pertence_diamond = mpatches.RegularPolygon((6, 4.5), 4, radius=0.5,
                                             facecolor=cor_relacionamento, edgecolor=cor_rel_borda, linewidth=2)
    ax.add_patch(pertence_diamond)
    ax.text(6, 4.5, 'PERTENCE', fontsize=9, fontweight='bold', ha='center')
    
    # Linhas de relacionamento
    # User -> POSSUI
    ax.plot([3, 4], [6.75, 6.75], 'k-', linewidth=2)
    # POSSUI -> Category
    ax.plot([5, 6], [6.75, 6.75], 'k-', linewidth=2)
    
    # User -> REALIZA
    ax.plot([2, 2.5], [6, 5], 'k-', linewidth=2)
    # REALIZA -> Transaction
    ax.plot([2.5, 3.5], [4, 2.75], 'k-', linewidth=2)
    
    # Transaction -> PERTENCE
    ax.plot([5.5, 6], [2.75, 4], 'k-', linewidth=2)
    # PERTENCE -> Category
    ax.plot([6, 7], [5, 6], 'k-', linewidth=2)
    
    # Cardinalidades
    ax.text(3.2, 7, '1', fontsize=12, fontweight='bold')
    ax.text(5.8, 7, 'N', fontsize=12, fontweight='bold')
    ax.text(1.7, 5.5, '1', fontsize=12, fontweight='bold')
    ax.text(3.2, 3.2, 'N', fontsize=12, fontweight='bold')
    ax.text(5.2, 3.2, 'N', fontsize=12, fontweight='bold')
    ax.text(7.3, 5.5, '1', fontsize=12, fontweight='bold')
    
    # Título
    ax.text(5, 7.7, 'MODELO ENTIDADE-RELACIONAMENTO (MER)', fontsize=16, fontweight='bold', ha='center')
    ax.text(5, 7.4, 'RuViPay - Sistema de Gestão Financeira', fontsize=12, ha='center', style='italic')
    
    # Atributos principais
    ax.text(1, 5.3, '• id\n• username\n• email\n• full_name', fontsize=9, va='top')
    ax.text(6, 5.3, '• id\n• name\n• type\n• color', fontsize=9, va='top')
    ax.text(3.5, 1.3, '• id\n• description\n• amount\n• date', fontsize=9, va='top')
    
    plt.tight_layout()
    return fig

def criar_caso_uso():
    """Cria o Diagrama de Casos de Uso"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Sistema
    sistema_rect = mpatches.Rectangle((3, 1), 6, 8, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(sistema_rect)
    ax.text(6, 9.3, 'SISTEMA RUVIOPAY', fontsize=14, fontweight='bold', ha='center')
    
    # Ator
    ax.text(1, 5, '👤', fontsize=30, ha='center')
    ax.text(1, 4.5, 'Usuário', fontsize=12, fontweight='bold', ha='center')
    
    # Casos de uso
    casos_uso = [
        (6, 8, 'Fazer Login'),
        (6, 7.2, 'Registrar-se'),
        (4.5, 6.4, 'Gerenciar\nCategorias'),
        (7.5, 6.4, 'Adicionar\nTransação'),
        (4.5, 5.2, 'Editar\nTransação'),
        (7.5, 5.2, 'Excluir\nTransação'),
        (4.5, 4, 'Visualizar\nRelatórios'),
        (7.5, 4, 'Filtrar\nTransações'),
        (6, 2.8, 'Visualizar Dashboard'),
        (6, 2, 'Exportar Dados')
    ]
    
    # Desenhar casos de uso
    for x, y, texto in casos_uso:
        elipse = mpatches.Ellipse((x, y), 1.4, 0.6, facecolor='lightblue', edgecolor='blue')
        ax.add_patch(elipse)
        ax.text(x, y, texto, fontsize=9, ha='center', va='center', fontweight='bold')
        
        # Linha conectando ao usuário
        ax.plot([2, x-0.7], [5, y], 'k-', linewidth=1)
    
    # Relacionamentos Include/Extend
    ax.annotate('', xy=(6, 7.8), xytext=(6, 7.4),
                arrowprops=dict(arrowstyle='-->', lw=1, color='red'))
    ax.text(6.5, 7.6, '<<include>>', fontsize=8, style='italic', color='red')
    
    # Título
    ax.text(6, 0.5, 'DIAGRAMA DE CASOS DE USO - RuViPay', fontsize=16, fontweight='bold', ha='center')
    
    plt.tight_layout()
    return fig

def criar_diagramas_tcc():
    """Função principal que cria todos os diagramas"""
    
    # Criar diretório para salvar diagramas
    output_dir = Path("documentacao_tcc")
    output_dir.mkdir(exist_ok=True)
    
    print("🎨 GERANDO DIAGRAMAS PARA TCC...")
    print("=" * 40)
    
    # Diagrama de Classes
    print("📊 Criando Diagrama de Classes...")
    fig_classes = criar_diagrama_classes()
    fig_classes.savefig(output_dir / "diagrama_classes.png", dpi=300, bbox_inches='tight')
    fig_classes.savefig(output_dir / "diagrama_classes.pdf", bbox_inches='tight')
    plt.close(fig_classes)
    
    # MER/DER
    print("🗄️ Criando Modelo Entidade-Relacionamento...")
    fig_mer = criar_mer_der()
    fig_mer.savefig(output_dir / "modelo_er.png", dpi=300, bbox_inches='tight')
    fig_mer.savefig(output_dir / "modelo_er.pdf", bbox_inches='tight')
    plt.close(fig_mer)
    
    # Casos de Uso
    print("👥 Criando Diagrama de Casos de Uso...")
    fig_casos = criar_caso_uso()
    fig_casos.savefig(output_dir / "casos_de_uso.png", dpi=300, bbox_inches='tight')
    fig_casos.savefig(output_dir / "casos_de_uso.pdf", bbox_inches='tight')
    plt.close(fig_casos)
    
    print(f"\n✅ DIAGRAMAS CRIADOS COM SUCESSO!")
    print(f"📁 Salvos em: {output_dir.absolute()}")
    print("\n📋 ARQUIVOS GERADOS:")
    print("   • diagrama_classes.png/pdf")
    print("   • modelo_er.png/pdf")
    print("   • casos_de_uso.png/pdf")

if __name__ == "__main__":
    criar_diagramas_tcc()