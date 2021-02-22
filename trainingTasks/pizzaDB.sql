-- Spørringer
-- 1
select navn, adresse
from kunde 
where postnr = 7000;

-- 2
select count(*) as "Antall kunder"
from kunde;

-- 3
select distinct poststed
from poststeder
order by poststed asc;

-- 4
select kid, navn, adresse, postnr, poststed
from kunde natural join poststeder;

-- 5
select navn, count(antall) as "Antall", sum(delsum) as "Sum"
from pizzatyper inner join ordrelinje on pid = pizza
where navn = "Thai Chicken";

-- 6
select distinct navn
from pizzatyper inner join ordrelinje on pid = pizza
order by navn asc; 

-- 7
select kid, navn, adresse
from kunde
where adresse like "%gata%";

-- 8
select p.navn
from pizzatyper as p
where pid not in (
	select pizza
    from (kunde inner join ordre on kunde.kid = ordre.kunde)
	inner join ordrelinje on ordre.ordrenr = ordrelinje.ordrenr
	where kunde.navn = "Kari");
    
-- 9
select navn from kunde union select navn from pizzatyper;

-- 10
select p.postnr, poststed, count(kid) as antall
from poststeder as p left outer join kunde as k on p.postnr = k.postnr
group by p.postnr
order by antall desc;

-- 11
select kid, navn
from kunde 
where kid not in (
	select kid 
    from (kunde inner join ordre on kid = kunde) 
    inner join ordrelinje on ordre.ordrenr = ordrelinje.ordrenr 
    inner join pizzatyper on pizza = pid
    where pizzatyper.navn = "Thai Chicken");
    
-- Innsetting, oppdatering og sletting
-- Oppgave 1
insert into ordre 
values (6, "2014-01-30", null, 998, 2);

insert into ordrelinje
values (6, 1, 3, 1, 228), (6, 2, 4, 3, 762);

-- Oppgave 2
update pizzatyper
set pris = pris*1.10;

-- Oppgave 3
delete from pizzatyper
where navn = "Thai Chicken";
-- ERROR 1217 (23000): Cannot delete or update a parent row: a foreign key constraint fails
-- En slik sletting vil bryte med referanseintegritet i noen ordrelinjer. 
-- Disse linjene må dermed slettes først. 
