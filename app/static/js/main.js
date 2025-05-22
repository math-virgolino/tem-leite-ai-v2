// main.js - Funcionalidades JavaScript para o sistema "Tem Leite Aí?"

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Função para rolar para o final do chat
    function scrollChatToBottom() {
        var chatMessages = document.getElementById('chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Rolar para o final do chat quando a página carregar
    scrollChatToBottom();

    // Validação de formulários
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Função para formatar CEP
    function formatCEP() {
        var cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('input', function(e) {
                var value = e.target.value.replace(/\D/g, '');
                if (value.length > 5) {
                    value = value.substring(0, 5) + '-' + value.substring(5, 8);
                }
                e.target.value = value;
            });
        }
    }

    // Inicializar formatação de CEP
    formatCEP();

    // Função para confirmar ações importantes
    function setupConfirmations() {
        var confirmButtons = document.querySelectorAll('.confirm-action');
        confirmButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm('Tem certeza que deseja realizar esta ação?')) {
                    e.preventDefault();
                }
            });
        });
    }

    // Inicializar confirmações
    setupConfirmations();

    // Função para marcar mensagens como lidas via AJAX
    function setupMessageReadMarking() {
        var chatLinks = document.querySelectorAll('.conversation-item');
        chatLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                var messageId = this.getAttribute('data-message-id');
                if (messageId) {
                    fetch('/marcar_como_lida/' + messageId)
                        .then(response => {
                            if (response.ok) {
                                var badge = this.querySelector('.badge-unread');
                                if (badge) {
                                    badge.style.display = 'none';
                                }
                                this.classList.remove('unread');
                            }
                        })
                        .catch(error => console.error('Erro ao marcar mensagem como lida:', error));
                }
            });
        });
    }

    // Inicializar marcação de mensagens como lidas
    setupMessageReadMarking();

    // Animações para elementos da página inicial
    function setupHomeAnimations() {
        var featureBoxes = document.querySelectorAll('.feature-box');
        if (featureBoxes.length > 0) {
            // Adicionar classe para animar entrada dos elementos
            setTimeout(function() {
                featureBoxes.forEach(function(box, index) {
                    setTimeout(function() {
                        box.classList.add('animated');
                    }, index * 200);
                });
            }, 500);
        }
    }

    // Inicializar animações da página inicial
    setupHomeAnimations();

    // Função para validar quantidade de doação
    function validateDonationAmount() {
        var quantidadeInput = document.getElementById('quantidade');
        if (quantidadeInput) {
            quantidadeInput.addEventListener('input', function() {
                var value = parseFloat(this.value);
                if (isNaN(value) || value <= 0) {
                    this.setCustomValidity('A quantidade deve ser maior que zero.');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
    }

    // Inicializar validação de quantidade de doação
    validateDonationAmount();

    // Função para atualizar contador de caracteres em mensagens
    function setupMessageCounter() {
        var messageTextarea = document.querySelector('textarea[name="conteudo"]');
        if (messageTextarea) {
            var counterElement = document.createElement('div');
            counterElement.className = 'text-muted small mt-1';
            counterElement.id = 'character-counter';
            messageTextarea.parentNode.appendChild(counterElement);
            
            function updateCounter() {
                var remaining = 1000 - messageTextarea.value.length;
                counterElement.textContent = remaining + ' caracteres restantes';
                if (remaining < 50) {
                    counterElement.classList.add('text-danger');
                } else {
                    counterElement.classList.remove('text-danger');
                }
            }
            
            messageTextarea.addEventListener('input', updateCounter);
            updateCounter(); // Inicializar contador
        }
    }

    // Inicializar contador de caracteres
    setupMessageCounter();
});
