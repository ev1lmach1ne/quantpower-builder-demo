// El índice queda accesible sin JavaScript; en móvil empieza plegado.
const navigation = document.querySelector('.help-sidebar details');
if (navigation && window.matchMedia('(max-width: 820px)').matches) {
  navigation.open = false;
}
