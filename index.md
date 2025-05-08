
# Hi, I'm Steven

Cybersecurity Student | Navy Veteran | Lifelong Learner

## About Me

I’m a Navy veteran and former construction supervisor, with experience managing logistics and operations at Domino’s. Now transitioning into cybersecurity, I bring discipline, leadership, and a passion for lifelong learning to every challenge I take on.

## Certifications

{% for cert in site.data.certifications %}
[![{{ cert.name }}]({{ cert.icon }})]({{ cert.link | default: '#' }})
{% endfor %}

## Lab Projects

- [Active Directory Lab 1.0](https://github.com/sloucks623/active-directory-lab-1.0)
- [Active Directory Lab 2.0](https://github.com/sloucks623/active-directory-lab-2.0)
- [SOC Automation Lab](https://github.com/sloucks623/lab-soc-automation)
- [MITRE ATT&CK Blog](/blog/mitre-attack)
