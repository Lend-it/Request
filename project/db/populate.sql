\c requestlenditdb_dev

INSERT INTO public.product_category
  (name)
VALUES
  ('Eletrodomésticos'),
  ('Livros e revistas'),
  ('Eletrônicos'),
  ('Ferramentas'),
  ('Jogos');

INSERT INTO public.request
  (requestid,productname,startdate,enddate,description,requester,lender,finalized)
VALUES
	 ('8d27b6c1-ac8a-4f29-97b0-96cef6938267','Harry Potter e a Câmara Secreta','2019-09-21','2019-10-10','Eu tenho a coleção do Harry Potter, mas meu cachorro comeu boa parte desse livro e gostaria dele emprestado para poder reler a série, pois não pretendo comprar novamente.','rogerio@email.com','lucas@email.com',false),
	 ('fce61c6d-1cb0-488c-a2fa-6a90fdbe192d','Furadeira','2020-01-04','2020-01-10','Preciso furar as cortinas e os suportes da televisão do meu apartamento e gostaria emprestado! Alguém pode me ajudar?','esio@email.com','rogerio@email.com',false),
	 ('1c1ad4cd-ce57-485d-bc6c-72941386bc99','Secador de Cabelo','2020-04-03','2020-04-04','Meu secador queimou e minha festa de formatura é hoje!! Alguém pode me emprestar um pra eu poder arrumar meu topete? É urgenteee!','youssef@email.com','rogerio@email.com',true),
	 ('63f9ea52-c81e-4279-91f4-c5d61d2e9c31','Airfryer','2020-09-02','2020-09-05','Vou receber uns amigos durantes esses dias e gostaria de uma emprestada para preparar alguns peticos. Alguém pode me emprestar?','lucas@email.com','youssef@email.com',true),
	 ('9406ab9c-a0e2-4ec3-8779-a45ec7788f7c','PlayStation 3','2021-02-14','2021-02-21','Meus primos vão passar uma semana aqui em casa e meu PS3 tá estragado. Sem PS3 não dá pra receber eles. Alguém poderia me emprestar durante essa semana?','youssef@email.com','esio@email.com',false);