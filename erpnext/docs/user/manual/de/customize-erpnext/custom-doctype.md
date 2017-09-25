# Benutzerdefinierter DocType
<span class="text-muted contributed-by">Beigetragen von CWT Connector & Wire Technology GmbH</span>

Ein DocType oder Dokumententyp wird dazu verwendet Formulare in ERPNext einzufügen. Formulare wie Kundenauftrag, Ausgangsrechnung und Fertigungsauftrag werden im Hintergrund als DocType verarbeitet. Nehmen wir an, dass wir für ein Buch einen benutzerdefinierten DocType erstellen.

Ein benutzerspezifischer DocType erlaubt es Ihnen nach Ihren Bedürfnissen benutzerspezifische Formulare in ERPNext einzufügen.

Um einen neuen DocType zu erstellen, gehen Sie zu:

> Einstellungen > Anpassen > Doctype > Neu

### Einzelheiten zum DocType

1. Modul: Wählen Sie das Modul aus, in dem dieser DocType verwendet wird.
2. Dokumententyp: Geben Sie an, ob dieser DocType Hauptdaten befördern oder Transaktionen nachverfolgen soll. Der DocType für das Buch wird als Vorlage hinzugefügt.
3. Ist Untertabelle: Wenn dieser DocType als Tabelle in einen anderen DocType eingefügt wird, wie die Artikeltabelle in den DocType Kundenauftrag, dann sollten Sie auch "Ist Untertabelle" ankreuzen. Ansonsten nicht.
4. Ist einzeln: Wenn diese Option aktiviert ist, wird dieser DocType zu einem einzeln verwendeten Formular, wie die Vertriebseinstellungen, die nicht von Benutzern reproduziert werden können.
5. Benutzerdefiniert?: Dieses Feld ist standardmäßig aktiviert, wenn ein benutzerdefinierter DocType hinzugefügt wird.

<<<<<<< HEAD
![Grundlagen zum Doctype](/docs/assets/img/setup/customize/doctype-basics.png)
=======
![Grundlagen zum Doctype]({{docs_base_url}}/assets/img/setup/customize/doctype-basics.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Felder

In der Tabelle Felder können Sie die Felder (Eigenschaften) des DocTypes (Artikel) hinzufügen.

Felder sind viel mehr als Datenbankspalten; sie können sein:

1. Spalten in der Datenbank
2. Wichtig für das Layout (Bereiche, Spaltentrennung)
3. Untertabellen (Feld vom Typ Tabelle)
4. HTML
5. Aktionen (Schaltflächen)
6. Anhänge oder Bilder

<<<<<<< HEAD
![Felder im DocType](/docs/assets/img/setup/customize/Doctype-all-fields.png)
=======
![Felder im DocType]({{docs_base_url}}/assets/img/setup/customize/Doctype-all-fields.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

Wenn Sie Felder hinzufügen, müssen Sie den **Typ** angeben. Für eine Bereichs- oder Spaltentrennung  ist die **Bezeichnung** optional. Der **Name** (Feldname) ist der Name der Spalte in der Datenbank.

Sie können auch weitere Einstellungen des Feldes eingeben, so z. B. ob es zwingend erforderlich ist, schreibgeschützt, usw.

### Benennung

In diesem Abschnitt können Sie Kriterien definieren nach denen Dokumente dieses DocTypes benannt werden. Es gibt viele verschiedene Kriterien nach denen ein Dokument benannt werden kann, wie z. B. dem Wert in diesem spezifischen Feld, oder die Benamungsserie, oder der Wert der vom Benutzer an der Eingabeaufforderung eingegeben wird, die angezeit wird, wenn ein Dokument abgespeichert wird. Im folgenden Beispiel benennen wir auf Grundlage des Wertes im Feld **book_name**.

<<<<<<< HEAD
![Bezeichnung von DocTypes](/docs/assets/img/setup/customize/doctype-field-naming.png)
=======
![Bezeichnung von DocTypes]({{docs_base_url}}/assets/img/setup/customize/doctype-field-naming.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Berechtigung

In dieser Tabelle können Sie Rollen und Berechtigungs-Rollen für diese für die betreffenden DocTypes auswählen.

<<<<<<< HEAD
![Berechtigungen bei DocTypes](/docs/assets/img/setup/customize/Doctype-permissions.png)
=======
![Berechtigungen bei DocTypes]({{docs_base_url}}/assets/img/setup/customize/Doctype-permissions.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### DocTypes abspeichern

Wenn Sie einen DocType abspeichern, erscheint ein Popup-Fenster über welches Sie den Namen des DocTypes eingeben können.

<<<<<<< HEAD
![DocTypes speichern](/docs/assets/img/setup/customize/Doctype-save.png)
=======
![DocTypes speichern]({{docs_base_url}}/assets/img/setup/customize/Doctype-save.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Der DocType im System

Um den DocType zu aktivieren, öffnen Sie das Modul, welches Sie für den DocType definiert haben. Da wird den DocType "Books" im Modul Personalwesen erstellt haben, gehen Sie hierhin um Zugriff zu erhalten:

> Personalwesen > Dokumente > Buch

<<<<<<< HEAD
![Übersicht der DocTypes](/docs/assets/img/setup/customize/Doctype-list-view.png)
=======
![Übersicht der DocTypes]({{docs_base_url}}/assets/img/setup/customize/Doctype-list-view.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

### Buchvorlage

Wenn Sie die Felder ausfüllen, schaut das ganze dann so aus.

<<<<<<< HEAD
![Übersicht der DocTypes](/docs/assets/img/setup/customize/Doctype-book-added.png)
=======
![Übersicht der DocTypes]({{docs_base_url}}/assets/img/setup/customize/Doctype-book-added.png)
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347

{next}
