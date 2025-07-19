# Classe responsável por enviar notificações (atualmente via impressão).

class NotificacaoService:
    def enviar_notificacao(self, mensagem: str):
        # Por enquanto, apenas imprime; depois pode virar email, push, fila etc.
        print(f"[Notificação] {mensagem}")
