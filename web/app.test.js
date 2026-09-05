const test = require("node:test");
const assert = require("node:assert/strict");
const { formatearEuros, calcularResumen } = require("./app");

test("calcula propina, total y por persona correctamente", () => {
  const r = calcularResumen(50, 10, 2);
  assert.equal(r.error, undefined);
  assert.equal(r.propina, 5);
  assert.equal(r.total, 55);
  assert.equal(r.porPersona, 27.5);
});

test("divide correctamente entre número de personas", () => {
  const r = calcularResumen(80, 20, 4);
  assert.equal(r.error, undefined);
  assert.equal(r.porPersona, 24);
});

test("valida cuenta inválida o cero", () => {
  assert.equal(calcularResumen(0, 10, 2).error, "Introduce un importe de cuenta válido.");
  assert.equal(calcularResumen(Number.NaN, 10, 2).error, "Introduce un importe de cuenta válido.");
});

test("valida porcentaje negativo", () => {
  assert.equal(calcularResumen(50, -1, 2).error, "Introduce un porcentaje de propina válido.");
});

test("valida personas menores que 1 y no entero", () => {
  assert.equal(calcularResumen(50, 10, 0).error, "El número de personas debe ser un entero de al menos 1.");
  assert.equal(calcularResumen(50, 10, 1.5).error, "El número de personas debe ser un entero de al menos 1.");
});

test("formatea moneda en euros", () => {
  assert.equal(formatearEuros(27.5), "27,50 €");
});
