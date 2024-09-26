import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Produto, MovimentoEstoque, Fornecedor
from .forms import LoginForm, RegistrationForm, ProdutoForm, MovimentoEstoqueForm, FornecedorForm, UsuarioForm

def home(request):
    return render(request, 'index.html')

# View de login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial após o login
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# View de registro
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

# View para cadastrar produto
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

# View para listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'lista_produtos.html', {'produtos': produtos})

# View para movimentação de estoque
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_movimentos')
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'movimentar_estoque.html', {'form': form})

# View para listar movimentações de estoque
def lista_movimentos(request):
    movimentos = MovimentoEstoque.objects.all()
    return render(request, 'lista_movimentos.html', {'movimentos': movimentos})

# Cadastro de Fornecedores
def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'cadastrar_fornecedor.html', {'form': form})

# Consulta de Fornecedores
def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'lista_fornecedores.html', {'fornecedores': fornecedores})

# Função auxiliar para gerar PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=400)
    return response

# Relatório de Entrada e Saída de Produtos
def relatorio_entrada_saida(request):
    movimentos = MovimentoEstoque.objects.all()
    
    # Se o usuário solicitar a geração de PDF
    if request.GET.get('format') == 'pdf':
        context = {'movimentos': movimentos}
        pdf = render_to_pdf('relatorio_entrada_saida_pdf.html', context)
        return pdf
    
    # Caso contrário, renderiza a página HTML normal
    return render(request, 'relatorio_entrada_saida.html', {'movimentos': movimentos})

# Relatório de Validade de Produtos
def relatorio_validade_produtos(request):
    produtos = Produto.objects.filter(data_validade__lt=timezone.now())
    return render(request, 'relatorio_validade_produtos.html', {'produtos': produtos})

# Histórico de Movimentações
def historico_movimentacoes(request):
    movimentos = MovimentoEstoque.objects.all()
    return render(request, 'historico_movimentacoes.html', {'movimentos': movimentos})

# Cadastrar Usuários
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'cadastrar_usuario.html', {'form': form})

# Lista de Usuários
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

# Logout do usuário
def logout_view(request):
    logout(request)
    return redirect('login')

# Nova view para o inventário
def inventario_view(request):
    # Aqui você pode adicionar a lógica para buscar os produtos ou movimentações que deseja exibir no inventário
    produtos = Produto.objects.all()  # Exemplo: busca todos os produtos
    return render(request, 'inventario.html', {'produtos': produtos})  # Renderiza a página de inventário