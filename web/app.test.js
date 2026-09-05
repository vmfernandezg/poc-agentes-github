const test = require("node:test");
const assert = require("node:assert/strict");
const {
  formatearEuros,
  calcularResumen,
  convertirDivisa,
  cuotaPrestamo,
  dividirGastos,
  mesesAhorro,
} = require("./app");

const cerca = (a, b, tol = 1e-9) => assert.ok(Math.abs(a - b) < tol, `${a} ≈ ${b}`);

// ---------- Propina ----------
test("propina: calcula propina, total y por persona", () => {
  const r = calcularResumen(50, 10, 2);
  assert.equal(r.error, undefined);
  assert.equal(r.propina, 5);
  assert.equal(r.total, 55);
  assert.equal(r.porPersona, 27.5);
});

test("propina: divide entre el número de personas", () => {
  assert.equal(calcularResumen(80, 20, 4).porPersona, 24);
});

test("propina: valida entradas inválidas", () => {
  assert.equal(calcularResumen(0, 10, 2).error, "Introduce un importe de cuenta válido.");
  assert.equal(calcularResumen(50, -1, 2).error, "Introduce un porcentaje de propina válido.");
  assert.equal(calcularResumen(50, 10, 1.5).error, "El número de personas debe ser un entero de al menos 1.");
});

test("formatea moneda en euros", () => {
  // Intl usa un espacio fino sin ruptura (U+202F) según el ICU; lo normalizamos
  // a un espacio normal para que el test no dependa de la versión de Node.
  const s = formatearEuros(27.5).replace(/\s/g, " ");
  assert.equal(s, "27,50 €");
});

// ---------- Divisas ----------
test("divisas: convierte EUR a USD con la tasa de ejemplo", () => {
  const r = convertirDivisa(100, "EUR", "USD");
  assert.equal(r.error, undefined);
  cerca(r.resultado, 108);
  cerca(r.tasa, 1.08);
});

test("divisas: convierte EUR a MXN con la tasa de ejemplo", () => {
  const r = convertirDivisa(100, "EUR", "MXN");
  assert.equal(r.error, undefined);
  cerca(r.resultado, 1850);
  cerca(r.tasa, 18.5);
});

test("divisas: misma moneda devuelve el mismo importe", () => {
  const r = convertirDivisa(100, "EUR", "EUR");
  cerca(r.resultado, 100);
  cerca(r.tasa, 1);
});

test("divisas: importe negativo da error", () => {
  assert.equal(convertirDivisa(-5, "EUR", "USD").error, "Introduce un importe válido.");
});

// ---------- Préstamo ----------
test("préstamo: interés 0 reparte el principal en cuotas iguales", () => {
  const r = cuotaPrestamo(1200, 0, 12);
  assert.equal(r.error, undefined);
  assert.equal(r.cuota, 100);
  assert.equal(r.totalPagado, 1200);
  assert.equal(r.intereses, 0);
});

test("préstamo: con interés paga más que el principal", () => {
  const r = cuotaPrestamo(10000, 5, 12);
  assert.equal(r.error, undefined);
  assert.ok(r.intereses > 0);
  assert.ok(r.totalPagado > 10000);
});

test("préstamo: plazo inválido da error", () => {
  assert.equal(cuotaPrestamo(10000, 5, 0).error, "El plazo debe ser un número entero de meses (mínimo 1).");
});

// ---------- Dividir gastos ----------
test("gastos: divide sin propina", () => {
  const r = dividirGastos(120, 3, 0);
  assert.equal(r.error, undefined);
  cerca(r.totalConPropina, 120);
  cerca(r.porPersona, 40);
});

test("gastos: aplica propina y divide", () => {
  const r = dividirGastos(100, 4, 10);
  cerca(r.totalConPropina, 110);
  cerca(r.porPersona, 27.5);
});

test("gastos: personas inválidas da error", () => {
  assert.equal(dividirGastos(100, 0, 0).error, "El número de personas debe ser un entero de al menos 1.");
});

// ---------- Ahorro ----------
test("ahorro: sin interés, meses = meta / aporte redondeado hacia arriba", () => {
  const r = mesesAhorro(1000, 100, 0);
  assert.equal(r.error, undefined);
  assert.equal(r.meses, 10);
});

test("ahorro: con interés no tarda más que sin interés", () => {
  const r = mesesAhorro(1000, 100, 12);
  assert.equal(r.error, undefined);
  assert.ok(r.meses <= 10);
});

test("ahorro: aporte 0 da error", () => {
  assert.equal(mesesAhorro(1000, 0, 5).error, "El aporte mensual debe ser mayor que 0.");
});
