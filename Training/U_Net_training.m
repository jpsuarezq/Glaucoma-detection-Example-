%% datos

location = 'D:\Disco_Duro_JP\Archivos\Universidad\Pocesamiento digital de imagenes\Proyecto\Archivos\Seg';
data = imageDatastore(location, 'FileExtensions', '.png',...
                      'IncludeSubfolders',true, ...
                      'LabelSource','foldernames');
                  
%%
con=countEachLabel(data)
numTrainFiles = round((table2array(con(1,2))+table2array(con(2,2)))*0.08);
%%
[trainingDS, validationDS] = splitEachLabel (data, numTrainFiles, 'randomize' );
%

%%
% Convert labels to categoricals
trainingDS = data;
trainingDS.Labels = categorical(trainingDS.Labels);
validationgDS.Labels = categorical(validationDS.Labels);


%%
layers = [
    imageInputLayer([520 520 3])
    convolution2dLayer(3,8,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,16,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,32,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    fullyConnectedLayer(2)
    softmaxLayer
    classificationLayer];

%%
options = trainingOptions ( 'sgdm' , ... 
    'MaxEpochs',10,...
    'InitialLearnRate',1e-4, ...
    'Shuffle','every-epoch', ...
    'ValidationData',trainingDS, ...
    'ValidationFrequency',5, ...
    'Verbose',false, ...
    'MiniBatchSize',32, ...
    'Plots','training-progress');


trainedNet = trainNetwork(trainingDS,layers,options);

%%
YPred = classify(trainedNet,validationDS);
YValidation = validationDS.Labels;

accuracy = sum(YPred == YValidation)/numel(YValidation)
net_gla=trainedNet;

save ('net_gla','net_gla')

