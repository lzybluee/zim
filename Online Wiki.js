// ==UserScript==
// @name         Online Wiki
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  Press title text or 'w' key will link to online page
// @author       You
// @match        *://127.0.0.1:8080/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Your code here...
    function link2wiki() {
        window.open(document.querySelector(`link[rel='canonical']`).href);
    };

    let title_element = document.getElementById('firstHeading');

    if (!title_element) {
        for (const name of ['article-header', 'pcs-edit-section-title']) {
            const list = document.getElementsByClassName(name);
            if (list.length) {
                title_element = list[0];
                break;
            }
        }
    }

    title_element?.addEventListener('click', function(event) {
        if (window.getSelection().toString().length == 0) link2wiki();
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'w' || event.key === 'W') link2wiki();
    });
})();