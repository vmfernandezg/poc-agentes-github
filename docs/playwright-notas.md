# Notas rápidas de Playwright (@playwright/test)

## 1) Abrir una página
En un test, usa la fixture `page` y navega con `goto`:

```js
import { test, expect } from '@playwright/test';

test('abre una página', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);
});
```

## 2) Hacer clic por rol o por texto
- **Por rol** (recomendado para elementos interactivos):

```js
await page.getByRole('link', { name: 'Get started' }).click();
```

- **Por texto**:

```js
await page.getByText('orange').click();
```

## 3) Tomar un screenshot
Captura de toda la página o de un elemento:

```js
await page.screenshot({ path: 'screenshot.png' });
await page.locator('.header').screenshot({ path: 'header.png' });
```

---

**Biblioteca/fuente consultada en Context7:** `/microsoft/playwright` (Playwright), con snippets de `README.md`, `docs/src/writing-tests-js.md`, `docs/src/locators.md` y `docs/src/screenshots.md`.
