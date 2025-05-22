// Funcionalidades específicas para validação de formulários
document.addEventListener('DOMContentLoaded', function() {
    // Validação de formulário de registro
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        const passwordInput = registerForm.querySelector('input[name="password"]');
        const tipoSelect = registerForm.querySelector('select[name="tipo"]');
        
        // Validação de senha
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                if (this.value.length < 6) {
                    this.setCustomValidity('A senha deve ter pelo menos 6 caracteres');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        // Destacar tipo de usuário selecionado
        if (tipoSelect) {
            tipoSelect.addEventListener('change', function() {
                const infoText = document.getElementById('tipo-info');
                if (!infoText) {
                    const infoDiv = document.createElement('div');
                    infoDiv.id = 'tipo-info';
                    infoDiv.className = 'alert alert-info mt-2';
                    tipoSelect.parentNode.appendChild(infoDiv);
                }
                
                const infoDiv = document.getElementById('tipo-info');
                if (this.value === 'doador') {
                    infoDiv.innerHTML = '<i class="bi bi-info-circle-fill me-2"></i> Como doador, você poderá cadastrar doações de leite materno.';
                } else if (this.value === 'receptor') {
                    infoDiv.innerHTML = '<i class="bi bi-info-circle-fill me-2"></i> Como receptor, você poderá buscar doadores próximos e reservar doações.';
                } else {
                    infoDiv.innerHTML = '';
                }
            });
        }
    }
    
    // Melhorias para a busca de doadores
    const searchForm = document.querySelector('form[action*="buscar_doadores"]');
    if (searchForm) {
        const searchButton = searchForm.querySelector('button[type="submit"]');
        if (searchButton) {
            searchButton.addEventListener('click', function() {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Buscando...';
                this.disabled = true;
                searchForm.submit();
            });
        }
    }
    
    // Melhorias para o chat
    const chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
        // Auto-scroll para novas mensagens
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        // Adicionar indicador de digitação
        const chatForm = document.querySelector('.chat-form');
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator d-none';
        typingIndicator.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        chatContainer.appendChild(typingIndicator);
        
        // Simular indicador de digitação
        if (chatForm) {
            const textarea = chatForm.querySelector('textarea');
            if (textarea) {
                textarea.addEventListener('focus', function() {
                    // Simular que o outro usuário está digitando (apenas para demonstração)
                    setTimeout(function() {
                        typingIndicator.classList.remove('d-none');
                        setTimeout(function() {
                            typingIndicator.classList.add('d-none');
                        }, 3000);
                    }, 1000);
                });
            }
        }
    }
    
    // Melhorias para a confirmação de reserva
    const confirmForm = document.querySelector('form[action*="reservar_doacao"]');
    if (confirmForm) {
        const confirmButton = confirmForm.querySelector('button[type="submit"]');
        if (confirmButton) {
            confirmButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Adicionar modal de confirmação
                const modal = document.createElement('div');
                modal.className = 'modal fade';
                modal.id = 'confirmModal';
                modal.setAttribute('tabindex', '-1');
                modal.setAttribute('aria-labelledby', 'confirmModalLabel');
                modal.setAttribute('aria-hidden', 'true');
                
                modal.innerHTML = `
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="confirmModalLabel">Confirmar Reserva</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>Você está prestes a reservar esta doação. Após a confirmação, uma mensagem será enviada ao doador.</p>
                                <p>Deseja prosseguir?</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-success" id="confirmReserveBtn">Confirmar Reserva</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                const modalObj = new bootstrap.Modal(document.getElementById('confirmModal'));
                modalObj.show();
                
                document.getElementById('confirmReserveBtn').addEventListener('click', function() {
                    modalObj.hide();
                    confirmForm.submit();
                });
            });
        }
    }
    
    // Melhorias para a caixa de entrada
    const conversationItems = document.querySelectorAll('.conversation-item');
    conversationItems.forEach(function(item) {
        item.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s';
            this.style.transform = 'translateX(5px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
});
