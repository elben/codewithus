class MergesController < ApplicationController
  # GET /merges
  # GET /merges.xml
  def index
    @merges = Merge.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @merges }
    end
  end

  # GET /merges/1
  # GET /merges/1.xml
  def show
    @merge = Merge.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @merge }
    end
  end

  # GET /merges/new
  # GET /merges/new.xml
  def new
    @merge = Merge.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @merge }
    end
  end

  # GET /merges/1/edit
  def edit
    @merge = Merge.find(params[:id])
  end

  # POST /merges
  # POST /merges.xml
  def create
    @merge = Merge.new(params[:merge])

    respond_to do |format|
      if @merge.save
        format.html { redirect_to(@merge, :notice => 'Merge was successfully created.') }
        format.xml  { render :xml => @merge, :status => :created, :location => @merge }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @merge.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /merges/1
  # PUT /merges/1.xml
  def update
    @merge = Merge.find(params[:id])

    respond_to do |format|
      if @merge.update_attributes(params[:merge])
        format.html { redirect_to(@merge, :notice => 'Merge was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @merge.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /merges/1
  # DELETE /merges/1.xml
  def destroy
    @merge = Merge.find(params[:id])
    @merge.destroy

    respond_to do |format|
      format.html { redirect_to(merges_url) }
      format.xml  { head :ok }
    end
  end
end
