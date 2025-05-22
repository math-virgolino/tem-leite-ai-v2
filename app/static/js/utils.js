// Utilitários para melhorar a experiência do usuário
document.addEventListener('DOMContentLoaded', function() {
    // Animações de entrada para elementos da página
    function animateElements() {
        const elementsToAnimate = document.querySelectorAll('.feature-box, .card, .donor-card, .dashboard-card');
        
        elementsToAnimate.forEach((element, index) => {
            // Adicionar classe para animar com delay baseado no índice
            setTimeout(() => {
                element.classList.add('animated');
            }, 100 * index);
        });
    }
    
    // Iniciar animações
    animateElements();
    
    // Adicionar efeitos de hover em cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 15px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Melhorar acessibilidade de formulários
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        // Adicionar feedback visual ao focar
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('input-focused');
        });
    });
    
    // Adicionar contador de caracteres para campos de texto longos
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        if (!textarea.hasAttribute('data-has-counter')) {
            textarea.setAttribute('data-has-counter', 'true');
            
            const maxLength = textarea.getAttribute('maxlength') || 1000;
            const counterDiv = document.createElement('div');
            counterDiv.className = 'text-muted small text-end mt-1';
            counterDiv.innerHTML = `${maxLength - textarea.value.length} caracteres restantes`;
            
            textarea.parentElement.appendChild(counterDiv);
            
            textarea.addEventListener('input', function() {
                const remaining = maxLength - this.value.length;
                counterDiv.innerHTML = `${remaining} caracteres restantes`;
                
                if (remaining < 50) {
                    counterDiv.classList.add('text-danger');
                } else {
                    counterDiv.classList.remove('text-danger');
                }
            });
        }
    });
    
    // Adicionar efeitos de loading para botões de submit
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        if (!button.classList.contains('no-loading-effect')) {
            button.addEventListener('click', function() {
                const form = this.closest('form');
                
                if (form && form.checkValidity()) {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Processando...';
                    this.disabled = true;
                    
                    // Restaurar após um tempo se o formulário não for enviado
                    setTimeout(() => {
                        if (this.disabled) {
                            this.innerHTML = originalText;
                            this.disabled = false;
                        }
                    }, 5000);
                }
            });
        }
    });
    
    // Adicionar confirmação para ações importantes
    const dangerButtons = document.querySelectorAll('.btn-danger, .confirm-action');
    dangerButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.hasAttribute('data-confirmed')) {
                e.preventDefault();
                
                const action = this.getAttribute('data-action-name') || 'esta ação';
                
                if (confirm(`Tem certeza que deseja ${action}? Esta ação não pode ser desfeita.`)) {
                    this.setAttribute('data-confirmed', 'true');
                    this.click();
                }
            }
        });
    });
});
