window.LoaderManager = {
    overlay: null,  

    init: function() {
        this.overlay = document.getElementById('loadingOverlay');
        if (this.overlay) {
            this.overlay.style.display = 'none';
            this.overlay.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    },    

    show: function() {
        if (!this.overlay) this.init();        
        if (this.overlay) {
            this.overlay.style.display = 'block';
            this.overlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    },
    
    hide: function() {
        if (this.overlay) {
            this.overlay.classList.remove('show');
            setTimeout(() => {
                this.overlay.style.display = 'none';
                document.body.style.overflow = 'auto';
            }, 300);
        }
    },
    
    isVisible: function() {
        return this.overlay && (this.overlay.classList.contains('show') || this.overlay.style.display !== 'none');
    }
};

window.MatchingFormHandler = {
    init: function() {
        const form = document.getElementById('matchingForm');   
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }
        LoaderManager.hide();
        ButtonManager.enableSubmitButton();
        const hasResults = document.querySelector('#match-report');
        if (hasResults) {
            LoaderManager.hide();
            ButtonManager.enableSubmitButton();
        }
    },
    
    handleFormSubmit: function(e) {
        const warningElement = document.querySelector('.main-section__form-warning');
        if (warningElement) {
            return;
        }
        LoaderManager.show();
        ButtonManager.disableSubmitButton();
    }
};

function openDeletePopup(itemId, itemTitle, itemType) {
    const popup = document.getElementById('deletePopup');
    const form = document.getElementById('deleteForm');
    const title = document.getElementById('popup-title');

    title.textContent = `¿Eliminar "${itemTitle}"?`;
    form.action = `/profile/${itemType}/delete/${itemId}/`;
    popup.style.display = 'flex';
}

function closeDeletePopup() {
    document.getElementById('deletePopup').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    LoaderManager.init();
    if (document.getElementById('matchingForm')) {
        MatchingFormHandler.init();
    }
});