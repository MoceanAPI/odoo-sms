document.addEventListener('DOMContentLoaded', function() {
    var waitForElementToAppear = setInterval(function() {
        var menuBrandElement = document.querySelector('.o_menu_brand');
        if (menuBrandElement && menuBrandElement.textContent === 'MoceanAPI SMS') {
            var consentOverlay = document.createElement('div');
            consentOverlay.className = 'mc-consent-overlay';
            document.body.appendChild(consentOverlay);
            consentOverlay.style.display = 'none';

            window.cookieconsent.initialise({
                "revokeBtn": "<div class='cc-revoke cc-bottom cc-right cc-animate cc-color-override-688238583'>Data usage consent</div>",
                "palette": {
                    "popup": {
                        "background": "#000"
                    },
                    "button": {
                        "background": "#f1d600"
                    }
                },
                "position": "bottom-right",
                "type": "opt-in",
                "content": {
                    "message": "Help improve this plugin by sharing usage data!",
                    "dismiss": "Yes, I'd love to",
                    "deny": "Refuse",
                    "link": "Learn more!",
                    "allow": "Agree!",
                    "href": "https://moceanapi.com/legal/privacy"
                },
                onInitialise: function(status) {
                    if (status == cookieconsent.status.allow) myScripts();
                },
                onStatusChange: function(status) {
                    if (this.hasConsented()) myScripts();
                },
                onPopupOpen: function() {
                    consentOverlay.style.display = 'block';
                },
                onPopupClose: function() {
                    consentOverlay.style.display = 'none';
                }
            });
            
            clearInterval(waitForElementToAppear);
        }
    }, 250);
});

function myScripts() {
    (function(m, e, t, r, i, k, a) {
        m[i] = m[i] || function() {
            (m[i].a = m[i].a || []).push(arguments)
        };
        m[i].l = 1 * new Date();
        k = e.createElement(t), a = e.getElementsByTagName(t)[0];
        k.async = 1;
        k.src = r;
        a.parentNode.insertBefore(k, a)
    })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

    ym(89818200, "init", {
        clickmap: true,
        trackLinks: true,
        accurateTrackBounce: true,
        webvisor: true
    });
}
