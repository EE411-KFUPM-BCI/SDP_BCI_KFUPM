clc;                                    % incomplete program
clear;
close all;
% NOTE: the text files are huge, therefore it takes (2 ~ 6) sec to run.

 

% ---------------- read data from text file ----------------------------

 

data1 = readtable('C:\Users\abdulrahman\Downloads\data.txt');   % our data
       

 

% ---------------- Length of Tables ------------------------------------

 

H1 = height(data1);                         % for table "height used"
H2 = height(data2);                         % for table "height used"
H3 = height(data3);                         % for table "height used"

 

% ---------------- EEG into vector & array -------------------------------------

 

v1 = data1([2 : H1],2);                     % v1 >> vector1
v2 = data2([2 : H2],2);                     % v2 >> vector2
v3 = data3([2 : H3],2);                     % v2 >> vector2

 

array_v1 = table2array(v1);                 % convert to array for operations
array_v2 = table2array(v2);
array_v3 = table2array(v3);

 

% ---------------- Time setting -----------------------------------------

 

time1 = data1([2 : H1],23);                  % obtain from table
time2 = data2([2 : H2],23);
time3 = data3([2 : H3],23);

 

array_time1 = table2array(time1);            % convert to array for operations
array_time2 = table2array(time2);
array_time3 = table2array(time3);

 

L1 = length(array_time1);                  % Length measure for array
L2 = length(array_time2);
L3 = length(array_time3);

 

% ---------------- Operations on EEG ------------------------------------
% Scale Factor (Volts/count) = 1.2 Volts * 8388607.0 * 1.5 * 51.0;

 

%scaled_v1 = array_v1./(1.2 * 8388607.0 * 1.5 * 51.0)   ;       % to center it around 0 with 1 deviation
scaled_v1 = normalize(array_v1); 
scaled_v2 = normalize(array_v2); 
scaled_v3 = normalize(array_v3); 

 

% ---------------- Operations on Time -----------------------------------

 

% -------- time in Watch format to read --------------
duration1 = table2array(data1(H1,25)) - table2array(data1(2,25));
duration2 = table2array(data2(H2,25)) - table2array(data2(2,25));
duration3 = table2array(data3(H3,25)) - table2array(data3(2,25));

 

% -------- time in numbers format --------------------
period1 = array_time1(L1,1)-array_time1(2,1);  % period in seconds
period2 = array_time2(L2,1)-array_time2(2,1);        % period in seconds
period3 = array_time3(L3,1)-array_time3(3,1);        % period in seconds

 

% note obtained Milo data (period1) need to be devided by 100 to be in seconds ??
% ---------------- frequency & time --------------------
f1 = (H1-1)/period1;          % frequency = size of data / period it takes
t1 = 1/f1 ;  
f2 = (H2-1)/period2;          % frequency = size of data / period it takes
t2 = 1/f2 ;  
f3 = (H3-1)/period3;          % frequency = size of data / period it takes
t3 = 1/f3 ;  

 

 
% ---------------- additional operations -----------------------

 

 step_time1 = 0:t1:period1-t1;         % proposed time step
 LL1 = length(step_time1);          % length for operations
 i=0;
 % ------------- loop for cutting v1 to match the new time step --------
 for i = 1:LL1
     new_v1(i) = scaled_v1(i);              % assign to new_v1
 end  
  % ------------------  222 ----------------------------------
  step_time2 = 0:t2:period2-t2;         % proposed time step
 LL2 = length(step_time2);          % length for operations
 i=0;
 % ------------- loop for cutting v1 to match the new time step --------
 for i = 1:LL2
     new_v2(i) = scaled_v2(i);              % assign to new_v1
 end  
 % ------------------- 333 ------------------------
  step_time3 = 0:t3:period3-t3;         % proposed time step
 LL3 = length(step_time3);          % length for operations
 i=0;
 % ------------- loop for cutting v1 to match the new time step --------
 for i = 1:LL3
     new_v3(i) = scaled_v3(i);              % assign to new_v1
 end  

 

 
% ---------------------- Filter Settings ------------------------
FFT_data1 = fft(new_v1);                % Fourier tranform
FFT_data2 = fft(new_v2);                % Fourier tranform
FFT_data3 = fft(new_v3);                % Fourier tranform

 

   % ------------- setting single side spectrum parameters ---------
t11 = (0:LL1-1)*t1;                       
P2 = abs(FFT_data1/LL1);
P1 = P2(1:LL1/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f_para = f1*( 0:(LL1/2) )/LL1;
 % ------------------------- 222 --------------------------
t22 = (0:LL2-1)*t2;                       
P22 = abs(FFT_data2/LL2);
P12 = P22(1:LL2/2+1);
P12(2:end-1) = 2*P12(2:end-1);
f_para2 = f2*( 0:(LL2/2) )/LL2;
% ------------------------- 333 ---------------------------
t33 = (0:LL3-1)*t3;                       
P23 = abs(FFT_data3/LL3);
P13 = P23(1:LL3/2+1);
P13(2:end-1) = 2*P13(2:end-1);
f_para3 = f3*( 0:(LL3/2) )/LL3;

 

   % ------------- butterworth bandpass filter ---------------------

 


   
%    % sample frequency 250Hz, high pass filter cutoff frequency 5Hz
%    frq1 = 0.1 / 125;
%    [a1 b1] = butter(5 ,frq1 , 'high');
%     % filtt = fvtool (a1,b1);
%    filt1 = filter (a1,b1,P1);
%    
%    % sample frequency 250Hz, low pass filter cut off frequency 15Hz
%     frq2 = 15 / 125;
%    [a2 b2] = butter(5 ,frq2, 'Low');
%     %filtt = fvtool (a2,b2);
%    filt2 = filter (a2,b2,new_v1);
%    
%    FFT_data2 = fft(filt2); 
%    
%    t2 = (0:LL1-1)*t;           
% P22 = abs(FFT_data2/LL1);
% P12 = P22(1:LL1/2+1);
% P12(2:end-1) = 2*P12(2:end-1);
% ---------------------------------------------------------------------
% fnyq=f1/2;
% cut_high=10;
% cut_low=50;

 

% [b,a]= butter(4,[cut_high,cut_low]/fnyq,'bandpass');
% filtered_P1=filtfilt(b,a,P1);           % filtered signal 
% 
% % OR USE (filter) to be ( filtered_P1=filter(b,a,P1); )     % filtered signal 
% rec_filtered_P1=abs(filtered_P1);
% ------------------------- Ploting -------------------------------------
figure(1)
  bandpass(new_v1,[1 50], f1);  % filter and draw
figure(2)
  bandpass(new_v2,[1 50], f2);
figure(3)  
  bandpass(new_v3,[1 50], f3);
  
% figure(4)       % --- only presenting raw normlized data --- 
% subplot(2,1,1), plot(array_time1,scaled_v1);       % raw data with defected time
% subplot(2,1,2), plot(step_time1,new_v1);           % raw data with step time

 

figure(4)       % --- filtered signal plots -------
subplot(3,1,1),plot(f_para ,P1 ,'r'); xlim([1 65]);
title("Single-Sided Amplitude Spectrum of X(t)");xlabel("f (Hz)");ylabel("|P1(f)|");
subplot(3,1,2),plot(f_para2 ,P12 ,'r'); xlim([1 65]);
title("Single-Sided Amplitude Spectrum of X(t)");xlabel("f (Hz)");ylabel("|P1(f)|");
subplot(3,1,3),plot(f_para3 ,P13 ,'r'); xlim([1 65]);
title("Single-Sided Amplitude Spectrum of X(t)");xlabel("f (Hz)");ylabel("|P1(f)|");