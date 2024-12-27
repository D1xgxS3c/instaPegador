import instaloader
from getpass import getpass
import re
import os
import sys
from time import sleep
from colorama import Fore, Style, init

# Inicializa o colorama para suportar cores no terminal
init(autoreset=True, strip=True)

def animated_text(text, delay=0.05):
    """
    Exibe o texto caractere por caractere com um atraso.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    print()  # Nova linha após a animação

def display_header():
    """
    Exibe o cabeçalho estilizado com o nome D1xgxS3c e animação.
    """
    custom_ascii = f"""
{Fore.GREEN}
██████╗  ██╗██╗  ██╗ ██████╗ ██╗  ██╗███████╗██████╗  ██████╗
██╔══██╗███║╚██╗██╔╝██╔════╝ ╚██╗██╔╝██╔════╝╚════██╗██╔════╝
██║  ██║╚██║ ╚███╔╝ ██║  ███╗ ╚███╔╝ ███████╗ █████╔╝██║     
██║  ██║ ██║ ██╔██╗ ██║   ██║ ██╔██╗ ╚════██║ ╚═══██╗██║     
██████╔╝ ██║██╔╝ ██╗╚██████╔╝██╔╝ ██╗███████║██████╔╝╚██████╗
╚═════╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝
                                                             
    """
    animated_text(custom_ascii, delay=0.002)  # Anima o ASCII art
    animated_text(f"{Fore.RED}{Style.BRIGHT}Bem-vindo, D1xgxS3c!", delay=0.05)
    print("-" * 70)

def configure_instaloader():
    """
    Configura e retorna uma instância do Instaloader com as opções adequadas.
    """
    return instaloader.Instaloader(
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        filename_pattern='{profile}_{mediaid}'
    )

def login_instaloader(loader):
    """
    Realiza login no Instagram. Opcional, necessário para contas privadas.
    """
    try:
        username = input("Usuário: ")
        password = getpass("Senha: ")
        loader.login(username, password)
        print(f"{Fore.GREEN}Login realizado com sucesso!")
    except Exception as e:
        print(f"{Fore.RED}Erro no login: {e}")
        sys.exit(1)

def download_profile(loader, username, profile_pic_only=False):
    """
    Faz o download de um perfil, podendo incluir apenas a foto de perfil.
    """
    try:
        loader.download_profile(username, profile_pic_only=profile_pic_only)
        print(f"{Fore.GREEN}Download do perfil '{username}' concluído!")
    except Exception as e:
        print(f"{Fore.RED}Erro ao baixar perfil: {e}")

def download_posts(loader, username, download_dir="./downloads"):
    """
    Faz o download de todos os posts públicos de um perfil.
    """
    try:
        os.makedirs(download_dir, exist_ok=True)
        os.chdir(download_dir)
        profile = instaloader.Profile.from_username(loader.context, username)
        for post in profile.get_posts():
            loader.download_post(post, target=username)
        print(f"{Fore.GREEN}Todos os posts de '{username}' foram baixados!")
    except Exception as e:
        print(f"{Fore.RED}Erro ao baixar posts: {e}")

def download_post_by_url(loader, url, download_dir="./downloads"):
    """
    Faz o download de um post específico a partir da URL.
    """
    try:
        os.makedirs(download_dir, exist_ok=True)
        os.chdir(download_dir)
        shortcode_match = re.search(r'/p/([^/]+)/', url)
        if not shortcode_match:
            raise ValueError("URL inválida. Certifique-se de que é um link válido para um post.")
        
        shortcode = shortcode_match.group(1)
        print(f"{Fore.YELLOW}Baixando post com shortcode '{shortcode}'...")
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, ".")
        print(f"{Fore.GREEN}Download do post concluído!")
    except Exception as e:
        print(f"{Fore.RED}Erro ao baixar post por URL: {e}")

def display_menu():
    """
    Exibe o menu estilizado com animação.
    """
    menu_text = f"""
{Fore.CYAN}{Style.BRIGHT}Menu de Opções:
{Fore.YELLOW}[1] {Fore.WHITE}Baixar foto de perfil de um usuário
{Fore.YELLOW}[2] {Fore.WHITE}Baixar todos os posts de um usuário
{Fore.YELLOW}[3] {Fore.WHITE}Baixar post a partir de uma URL
{Fore.YELLOW}[0] {Fore.WHITE}Sair
    """
    animated_text(menu_text)

def main():
    """
    Função principal para gerenciar os downloads.
    """
    display_header()
    loader = configure_instaloader()

    # Login opcional, descomente se necessário para contas privadas
    # login_instaloader(loader)

    while True:
        display_menu()
        try:
            choice = int(input(f"{Fore.CYAN}Escolha uma opção: "))
            if choice == 1:
                username = input("Informe o nome de usuário: ")
                download_profile(loader, username, profile_pic_only=True)
            elif choice == 2:
                username = input("Informe o nome de usuário: ")
                download_posts(loader, username)
            elif choice == 3:
                url = input("Informe a URL do post: ")
                download_post_by_url(loader, url)
            elif choice == 0:
                print(f"{Fore.GREEN}Saindo... Até logo!")
                break
            else:
                print(f"{Fore.RED}Opção inválida!")
        except ValueError:
            print(f"{Fore.RED}Entrada inválida! Certifique-se de inserir um número.")
        except Exception as e:
            print(f"{Fore.RED}Erro: {e}")

if __name__ == "__main__":
    main()
