# Grammaire du langage Piscine (`.pisc`)

## 1. Introduction

Le langage **Piscine** est un langage minimaliste conçu dans le cadre du projet.
Il permet de **déclarer des variables**, d’**évaluer des expressions arithmétiques**, de faire des **conditions**, des **boucles** (`while` et `for`), et d’afficher des valeurs avec `print`.

La syntaxe est volontairement simple et inspirée de Python, C et JavaScript.
Cette section formalise la grammaire avec la notation **BNF (Backus–Naur Form)**.

---

## 2. Grammaire (BNF)

```bnf
<program> ::= <statement_list>

<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <assignment>
              | <print_stmt>
              | <if_stmt>
              | <while_stmt>
              | <for_stmt>
              | ε   ; (vide)

<assignment> ::= <identifier> "=" <expression>

<print_stmt> ::= "print" "(" <expression> ")"

<if_stmt> ::= "if" <expression> "{" <statement_list> "}"
              [ "else" "{" <statement_list> "}" ]

<while_stmt> ::= "while" <expression> "{" <statement_list> "}"

<for_stmt> ::= "for" <identifier> "in" "range" "(" <expression> ")" 
               "{" <statement_list> "}"

<expression> ::= <term> { ("+" | "-") <term> }

<term> ::= <factor> { ("*" | "/") <factor> }

<factor> ::= <number>
            | <string>
            | <boolean>
            | "null"
            | <identifier>
            | "(" <expression> ")"
            | "-" <factor>

<boolean> ::= "true" | "false"

<identifier> ::= <letter> { <letter> | <digit> | "_" }

<number> ::= <digit> { <digit> }

<string> ::= "\"" { <character> } "\""

<letter> ::= "a" | "b" | ... | "z" | "A" | ... | "Z"
<digit> ::= "0" | "1" | ... | "9"
<character> ::= any printable character except '"'
```

---

## 3. Explications des règles

* **Programme (`<program>`)** :
  Un fichier `.pisc` est une suite d’instructions.

* **Assignation (`<assignment>`)** :
  On affecte une valeur à une variable.
  Exemple :

  ```pisc
  a = 5
  b = a + 3
  ```

* **Affichage (`<print_stmt>`)** :
  Permet d’écrire sur la sortie standard.
  Exemple :

  ```pisc
  print(a)
  print("Hello")
  ```

* **Condition (`<if_stmt>`)** :
  Permet d’exécuter un bloc si une condition est vraie, avec éventuellement un `else`.
  Exemple :

  ```pisc
  if a < 10 {
      print("Petit")
  } else {
      print("Grand")
  }
  ```

* **Boucle `while` (`<while_stmt>`)** :
  Répète tant qu’une condition est vraie.
  Exemple :

  ```pisc
  while a < 5 {
      a = a + 1
      print(a)
  }
  ```

* **Boucle `for` (`<for_stmt>`)** :
  Répète un nombre de fois donné. Inspiré de Python.
  Exemple :

  ```pisc
  for i in range(3) {
      print(i)
  }
  ```

* **Expressions (`<expression>`)** :
  Supporte les opérateurs arithmétiques et de comparaison, avec respect des priorités.

  * Multiplication et division avant addition et soustraction.
  * Parenthèses possibles pour forcer un ordre.

  Exemple :

  ```pisc
  c = 2 + 3 * 4      # donne 14
  d = (2 + 3) * 4    # donne 20
  ```

* **Types supportés** :

  * `Number` : entiers (`0`, `42`)
  * `String` : texte entre guillemets (`"hello"`)
  * `Boolean` : `true` / `false`
  * `null` : valeur nulle

---

## 4. Exemples de programmes complets

### Exemple 1 : Affectations et print

```pisc
a = 5
b = 3
c = b * (4 + a)
print(c)  # Résultat attendu : 35
```

### Exemple 2 : Conditions

```pisc
x = 10
if x > 5 {
    print("x est grand")
} else {
    print("x est petit")
}
```

### Exemple 3 : Boucle While

```pisc
i = 0
while i < 5 {
    print(i)
    i = i + 1
}
```

### Exemple 4 : Boucle For

```pisc
for i in range(3) {
    print(i)
}
```
