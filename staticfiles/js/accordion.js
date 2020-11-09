function collapseSection(button) {
  var content = document.getElementById(button.getAttribute('data-target'));
  // get the height of the content's inner content, regardless of its actual size
  var sectionHeight = content.scrollHeight;
  
  // temporarily disable all css transitions
  var contentTransition = content.style.transition;
  content.style.transition = '';
  
  // on the next frame (as soon as the previous style change has taken effect),
  // explicitly set the content's height to its current pixel height, so we 
  // aren't transitioning out of 'auto'
  requestAnimationFrame(function() {
    content.style.height = sectionHeight + 'px';
    content.style.transition = contentTransition;
    
    // on the next frame (as soon as the previous style change has taken effect),
    // have the content transition to height: 0
    requestAnimationFrame(function() {
      content.style.height = 0 + 'px';
    });
  });
  
  // mark the section as "currently collapsed"
  button.setAttribute('aria-expanded', 'false');
}

function expandSection(button) {
  var content = document.getElementById(button.getAttribute('data-target'));
  // get the height of the content's inner content, regardless of its actual size
  var sectionHeight = content.scrollHeight;
  
  // have the content transition to the height of its inner content
  content.style.height = sectionHeight + 'px';

  // when the next css transition finishes (which should be the one we just triggered)
  content.addEventListener('transitionend', function(e) {
    // remove this event listener so it only gets triggered once
    content.removeEventListener('transitionend', arguments.callee);
    
    // remove "height" from the content's inline styles, so it can return to its initial value
    content.style.height = null;
  });
  
  // mark the section as "currently not collapsed"
  button.setAttribute('aria-expanded', 'true');
}



const buttons = document.querySelectorAll(".myaccordion button");

function toggleAccordion() {
    if (this.getAttribute('aria-expanded') == 'true')
        collapseSection(this);
    else
        expandSection(this);

    for (i = 0; i < buttons.length; i++) {
        if (buttons[i] != this && buttons[i].getAttribute('aria-expanded') == 'true')
            collapseSection(buttons[i]);
    }
}

buttons.forEach(function(button) {
    var content = document.getElementById(button.getAttribute('data-target'));
    content.style.height = '0px';
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', toggleAccordion)
});
