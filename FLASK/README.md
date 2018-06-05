# API

### Główna strona:
http://flask-env.gepn8fd8hx.eu-central-1.elasticbeanstalk.com/
Wszystkie adresy podane poniżej trzeba dopisać do tego adresu, po '/'.
Dane zwracane są jako JSONy. Nazwy kolumn i tablic są po angielsku.

### users/
#### GET:
wyświetla dane wszystkich użytkowników w formie:
`
    {
    "email": string (Unicode),  
    "id": int,
    "last_login_date": string (format daty: "2018-06-04"),
    "login": string (Unicode),
    "password": string (Unicode),
    "registration_date": string (format daty: "2018-06-04")
    },
    ...
`
#### POST: not implemented yet



### users/\<int:user_id\>
#### GET:
Wyświetla dane konkretnego usera o id = user_id, w takiej samej formie jak GET users/
#### PUT:
zmienia dane użytkownika o id = user_id na podstawie JSONa otrzymanego *w danej formie:*
`
  {
  "columns" : ['lista stringów', 'z nazwami kolumn do zmiany'],
  "values" : ['lista stringów', 'z wartościami na które mają się zmienić']
  }
`
**! UWAGA ! - kolejność elementów w obu listach musi się zgadzać! Tzn. jeżeli mamy columns : [1,2,3] i values : [a,b,c] to kolumna 1 = a, 2 = b, 3 = c.**

#### DELETE: not implemented yet


### users/\<int:user_id\>/subdomains/
#### GET:
wyświetla wszystkie subdomeny konkretnego użytkownika o id=user_id, w formie:
`
{
    "at": string (Unicode),
    "expiration_date": string (format daty: "2019-06-01"),
    "id_domain": int,
    "id_user": int,
    "ip_address": string (format: "77.65.89.81"),
    "name": "string (Unicode),
    "purchase_date": string (format daty: "2018-06-01"),
    "status": string (Unicode)"
},
 ...
`


### subdomains/
#### GET:
Wyświetla wszystkie subdomeny, w formie takiej jak w users/<int:user_id>/subdomains
#### POST:
Dodaje nową subdomenę, korzystając z danych przesłanych za pomocą JSONa w *takiej formie*:

    {
    "id_user" : int,
    "name" : string,
    "at" : string,
    "ip_address" : string (w formie '00.00.00.00'),
    "purchase_date" : data (w formie '2000-12-12'),
    "expiration_date" : data (w formie '2000-12-12')
    }
    
### subdomains/\<int:subdomain_id\>

#### PUT:
Edytuje subdomenę o id = subdomain_id korzystając z danych podanych w JSONie w *takiej formie jak przy  users/\<int:user_id\> [PUT]*

#### DELETE: not implemented yet
