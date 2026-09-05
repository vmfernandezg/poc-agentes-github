// Lógica de la calculadora de propina.
//
// Cálculo y validación de la calculadora de propina.

const $ = (id) => document.getElementById(id);

function formatearEuros(n) {
  return n.toLocaleString("es-ES", { style: "currency", currency: "EUR" });
}

function mostrarError(mensaje) {
  $("resultado").classList.add("oculto");
  const err = $("error");
  err.textContent = mensaje;
  err.classList.remove("oculto");
}

function actualizarBotonActivo(valor) {
  const porcentaje = Number(valor);
  document.querySelectorAll(".boton-propina").forEach((boton) => {
    const activo = Number(boton.dataset.porcentaje) === porcentaje;
    boton.classList.toggle("activo", activo);
    boton.setAttribute("aria-pressed", String(activo));
  });
}

function calcular(evento) {
  evento.preventDefault();

  const cuenta = Number($("cuenta").value);
  const porcentaje = Number($("porcentaje").value);
  const personas = Number($("personas").value);

  // Validación básica de entradas.
  if (!Number.isFinite(cuenta) || cuenta <= 0) {
    mostrarError("Introduce un importe de cuenta válido.");
    return;
  }
  if (!Number.isFinite(porcentaje) || porcentaje < 0) {
    mostrarError("Introduce un porcentaje de propina válido.");
    return;
  }
  if (!Number.isFinite(personas) || !Number.isInteger(personas) || personas < 1) {
    mostrarError("El número de personas debe ser un entero de al menos 1.");
    return;
  }

  const propina = cuenta * (porcentaje / 100);
  const total = cuenta + propina;
  const porPersona = total / personas;
  if (!Number.isFinite(propina) || !Number.isFinite(total) || !Number.isFinite(porPersona)) {
    mostrarError("Los valores son demasiado grandes para calcularse con precisión.");
    return;
  }

  $("error").classList.add("oculto");
  $("r-propina").textContent = formatearEuros(propina);
  $("r-total").textContent = formatearEuros(total);
  $("r-persona").textContent = formatearEuros(porPersona);
  $("resultado").classList.remove("oculto");
}

document.querySelectorAll(".boton-propina").forEach((boton) => {
  boton.addEventListener("click", () => {
    $("porcentaje").value = boton.dataset.porcentaje;
    actualizarBotonActivo(boton.dataset.porcentaje);
  });
});

$("porcentaje").addEventListener("input", (evento) => {
  actualizarBotonActivo(evento.target.value);
});

actualizarBotonActivo($("porcentaje").value);
document.getElementById("formulario").addEventListener("submit", calcular);
