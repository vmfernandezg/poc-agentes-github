# 🌐 Demo web estática + GitHub Pages

La carpeta `web/` es una **calculadora de propina** estática (HTML/CSS/JS) que se despliega
en **GitHub Pages** con el workflow `.github/workflows/deploy-pages.yml`.

## El bug de demo (a propósito)

En `web/app.js`, el **"Total por persona" NO divide entre el número de personas**:

```js
// BUG INTENCIONADO: se ignora "personas". Debería ser: total / personas
const porPersona = total;
```

Se ve a simple vista: cambias el nº de personas y el "por persona" no cambia.

## El ciclo completo (lo bonito de la v2)

```
1. Abres un issue: "El total por persona no se divide entre las personas"
2. Le pones la etiqueta auto-fix
3. El agente corrige-bugs arregla web/app.js y abre un PR
4. Revisas y haces merge
5. deploy-pages.yml redespliega  ->  ves el arreglo EN VIVO en la URL de Pages
```

## Activar Pages (una vez)

Pages debe usar **GitHub Actions** como origen:
**Settings → Pages → Build and deployment → Source: GitHub Actions.**

⚠️ **Nota importante:** GitHub Pages en repos **privados** requiere un **plan de pago**
(Pro/Team/Enterprise). Si tu repo es privado y estás en plan gratuito, tendrías que
**hacer el repo público** para publicar la web (o subir de plan).

La URL será aproximadamente: `https://vmfernandezg.github.io/poc-agentes-github/`
